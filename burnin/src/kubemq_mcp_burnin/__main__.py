from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from kubemq_mcp_burnin.config import load_config
from kubemq_mcp_burnin.runner import BurninRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="KubeMQ MCP Burn-in Suite")
    parser.add_argument(
        "--mode",
        choices=["smoke", "functional", "soak"],
        default=None,
        help="Run mode (overrides config file and BURNIN_MODE env var)",
    )
    parser.add_argument(
        "--duration",
        default=None,
        help="Soak duration, e.g. 15m, 1h (overrides config file)",
    )
    parser.add_argument(
        "--config",
        default="burnin-config.yaml",
        help="Path to config YAML (default: burnin-config.yaml)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    if args.mode:
        config.mode = args.mode
    if args.duration:
        config.duration = args.duration

    log_level = getattr(logging, config.output.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)-5s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    runner = BurninRunner(config)
    exit_code = asyncio.run(runner.run())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
