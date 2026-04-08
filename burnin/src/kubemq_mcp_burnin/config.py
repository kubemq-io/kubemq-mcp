from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ServerConfig:
    address: str = "http://localhost:9090"
    broker_address: str = "localhost:50000"


@dataclass
class EchoAgentConfig:
    count: int = 2


@dataclass
class SlowAgentConfig:
    count: int = 1
    delay_ms: int = 2000


@dataclass
class ErrorAgentConfig:
    count: int = 1
    error_rate: float = 1.0


@dataclass
class StreamingAgentConfig:
    count: int = 2
    events_per_stream: int = 10
    event_delay_ms: int = 100


@dataclass
class AgentsConfig:
    base_port: int = 18080
    echo: EchoAgentConfig = field(default_factory=EchoAgentConfig)
    slow: SlowAgentConfig = field(default_factory=SlowAgentConfig)
    error: ErrorAgentConfig = field(default_factory=ErrorAgentConfig)
    streaming: StreamingAgentConfig = field(default_factory=StreamingAgentConfig)


@dataclass
class SuitesConfig:
    mcp_core: bool = True
    mcp_bridge: bool = True
    mcp_protocol: bool = True
    mcp_soak: bool = False


@dataclass
class SoakConfig:
    rate: int = 50
    snapshot_interval: str = "30s"  # Reserved for future use
    channels_per_pattern: int = 2


@dataclass
class ThresholdsConfig:
    max_error_rate_pct: float = 1.0
    max_p99_latency_ms: float = 5000
    max_p999_latency_ms: float = 10000  # Reserved for future use
    min_throughput_pct: float = 90  # Reserved for future use


@dataclass
class OutputConfig:
    report_file: str = ""  # Reserved for future use
    log_level: str = "info"
    log_format: str = "text"  # Reserved for future use


@dataclass
class BurninConfig:
    version: str = "1"
    server: ServerConfig = field(default_factory=ServerConfig)
    mode: str = "functional"
    duration: str = "15m"
    agents: AgentsConfig = field(default_factory=AgentsConfig)
    suites: SuitesConfig = field(default_factory=SuitesConfig)
    soak: SoakConfig = field(default_factory=SoakConfig)
    thresholds: ThresholdsConfig = field(default_factory=ThresholdsConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    _VALID_MODES = ("smoke", "functional", "soak")

    def duration_seconds(self) -> int:
        unit_map = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        match = re.match(r"^(\d+)([smhd])$", self.duration)
        if not match:
            raise ValueError(f"Invalid duration format: {self.duration}")
        return int(match.group(1)) * unit_map[match.group(2)]

    def validate(self) -> None:
        """Validate config values at load time."""
        if self.mode not in self._VALID_MODES:
            raise ValueError(
                f"Invalid mode: {self.mode!r}. Must be one of {self._VALID_MODES}"
            )
        if not re.match(r"^\d+[smhd]$", self.duration):
            raise ValueError(f"Invalid duration format: {self.duration!r}")
        import logging
        valid_levels = ("debug", "info", "warning", "error", "critical")
        if self.output.log_level.lower() not in valid_levels:
            raise ValueError(
                f"Invalid log_level: {self.output.log_level!r}. "
                f"Must be one of {valid_levels}"
            )


def _build_nested(cls: type, data: dict[str, Any] | None) -> Any:
    if data is None:
        return cls()
    nested_fields: dict[str, type] = {}
    for f_name, f_type in cls.__dataclass_fields__.items():
        if hasattr(f_type.default_factory, "__call__"):
            factory = f_type.default_factory
            if hasattr(factory, "__dataclass_fields__"):
                nested_fields[f_name] = factory
    kwargs: dict[str, Any] = {}
    for k, v in data.items():
        if k in nested_fields and isinstance(v, dict):
            kwargs[k] = _build_nested(nested_fields[k], v)
        else:
            kwargs[k] = v
    return cls(**kwargs)


def load_config(path: str | None = None) -> BurninConfig:
    """Load config from YAML file, then apply environment variable overrides."""
    data: dict[str, Any] = {}
    if path:
        resolved = Path(path).resolve()
        if resolved.suffix not in (".yaml", ".yml"):
            raise ValueError(f"Config file must have .yaml or .yml extension: {path}")
        if resolved.exists():
            with open(resolved, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

    server_data = data.pop("server", {}) or {}
    agents_data = data.pop("agents", {}) or {}
    suites_data = data.pop("suites", {}) or {}
    soak_data = data.pop("soak", {}) or {}
    thresholds_data = data.pop("thresholds", {}) or {}
    output_data = data.pop("output", {}) or {}

    echo_data = agents_data.pop("echo", {}) or {}
    slow_data = agents_data.pop("slow", {}) or {}
    error_data = agents_data.pop("error", {}) or {}
    streaming_data = agents_data.pop("streaming", {}) or {}

    config = BurninConfig(
        version=data.get("version", "1"),
        mode=data.get("mode", "functional"),
        duration=data.get("duration", "15m"),
        server=ServerConfig(**server_data),
        agents=AgentsConfig(
            base_port=agents_data.get("base_port", 18080),
            echo=EchoAgentConfig(**echo_data),
            slow=SlowAgentConfig(**slow_data),
            error=ErrorAgentConfig(**error_data),
            streaming=StreamingAgentConfig(**streaming_data),
        ),
        suites=SuitesConfig(**suites_data),
        soak=SoakConfig(**soak_data),
        thresholds=ThresholdsConfig(**thresholds_data),
        output=OutputConfig(**output_data),
    )

    # KUBEMQ_MCP_URL and KUBEMQ_BROKER_ADDRESS are trusted operator inputs;
    # no scheme/host allowlist is applied — the burn-in targets whatever the
    # operator configures.
    if addr := os.environ.get("KUBEMQ_MCP_URL"):
        config.server.address = addr
    if addr := os.environ.get("KUBEMQ_BROKER_ADDRESS"):
        config.server.broker_address = addr
    if mode := os.environ.get("BURNIN_MODE"):
        config.mode = mode
    if dur := os.environ.get("BURNIN_DURATION"):
        config.duration = dur
    if level := os.environ.get("BURNIN_LOG_LEVEL"):
        config.output.log_level = level

    config.validate()
    return config
