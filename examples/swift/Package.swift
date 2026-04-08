// swift-tools-version: 6.0
import PackageDescription

let mcpDep: Target.Dependency = .product(name: "MCP", package: "swift-sdk")

let package = Package(
    name: "kubemq-mcp-swift-examples",
    platforms: [.macOS(.v13)],
    dependencies: [
        .package(url: "https://github.com/modelcontextprotocol/swift-sdk.git", from: "0.12.0"),
    ],
    targets: [
        .executableTarget(name: "QueueSend", dependencies: [mcpDep], path: "Sources/QueueSend"),
        .executableTarget(name: "QueueReceive", dependencies: [mcpDep], path: "Sources/QueueReceive"),
        .executableTarget(name: "QueuePeek", dependencies: [mcpDep], path: "Sources/QueuePeek"),
        .executableTarget(name: "EventsPublish", dependencies: [mcpDep], path: "Sources/EventsPublish"),
        .executableTarget(name: "EventsStorePublish", dependencies: [mcpDep], path: "Sources/EventsStorePublish"),
        .executableTarget(name: "EventsStoreRead", dependencies: [mcpDep], path: "Sources/EventsStoreRead"),
        .executableTarget(name: "EventsStoreReadLatest", dependencies: [mcpDep], path: "Sources/EventsStoreReadLatest"),
        .executableTarget(name: "CommandSend", dependencies: [mcpDep], path: "Sources/CommandSend"),
        .executableTarget(name: "QuerySend", dependencies: [mcpDep], path: "Sources/QuerySend"),
        .executableTarget(name: "ChannelList", dependencies: [mcpDep], path: "Sources/ChannelList"),
        .executableTarget(name: "ChannelInfo", dependencies: [mcpDep], path: "Sources/ChannelInfo"),
        .executableTarget(name: "AgentList", dependencies: [mcpDep], path: "Sources/AgentList"),
        .executableTarget(name: "AgentInfo", dependencies: [mcpDep], path: "Sources/AgentInfo"),
        .executableTarget(name: "AgentSend", dependencies: [mcpDep], path: "Sources/AgentSend"),
        .executableTarget(name: "AgentQuery", dependencies: [mcpDep], path: "Sources/AgentQuery"),
    ]
)
