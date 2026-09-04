#!/usr/bin/env python3
"""
AXIS Mesh Telemetry & Spatial Coordinate Processing Node
Author: Demien CAPSULECRAFT / BROADCIM INC
Architecture: Distributed UAV Mesh Telemetry & RF Spatial Coordinate Engine
"""

import math
import json
import time
import asyncio
from dataclasses import dataclass, asdict

@dataclass
class Coordinate3D:
    x: float
    y: float
    z: float

@dataclass
class TelemetryPacket:
    node_id: str
    timestamp: float
    origin: Coordinate3D
    neg_volume_block: float
    signal_metric_dbm: float

class SpatialMeshEngine:
    """
    Core processing engine for calculating 3D spatial coordinate vectors,
    invertible volume blocks, and RF mesh propagation metrics.
    """
    def __init__(self, node_id: str, origin_x: float = 0.0, origin_y: float = 0.0, origin_z: float = 0.0):
        self.node_id = node_id
        self.origin = Coordinate3D(x=origin_x, y=origin_y, z=origin_z)
        self.active_inventory = {}

    def calculate_distance(self, target: Coordinate3D) -> float:
        """Computes Euclidean distance from local node origin to target coordinate."""
        dx = target.x - self.origin.x
        dy = target.y - self.origin.y
        dz = target.z - self.origin.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def process_volume_block(self, length: float, width: float, height: float) -> float:
        """
        Computes the primary volume block and calculates the negative grid projection.
        Inverted value: -(topic.subject.block.volume)
        """
        volume = abs(length * width * height)
        neg_volume = -volume
        return neg_volume

    def ingest_telemetry(self, remote_node_id: str, x: float, y: float, z: float, signal_dbm: float) -> TelemetryPacket:
        """Ingests raw spatial coordinate telemetry and updates internal inventory state."""
        coord = Coordinate3D(x=x, y=y, z=z)
        neg_vol = self.process_volume_block(x, y, z)
        
        packet = TelemetryPacket(
            node_id=remote_node_id,
            timestamp=time.time(),
            origin=coord,
            neg_volume_block=neg_vol,
            signal_metric_dbm=signal_dbm
        )
        
        self.active_inventory[remote_node_id] = packet
        return packet

    def export_inventory_state(self) -> str:
        """Serializes active inventory state into JSON for upstream transport."""
        data = {
            "source_node": self.node_id,
            "local_origin": asdict(self.origin),
            "inventory": {k: asdict(v) for k, v in self.active_inventory.items()}
        }
        return json.dumps(data, indent=2)


async def main():
    node = SpatialMeshEngine(node_id="AXIS-NODE-01", origin_x=0.0, origin_y=0.0, origin_z=0.0)
    print("[+] Initializing AXIS Telemetry Ingestion Pipeline...")
    
    packet_a = node.ingest_telemetry("UAV-ALPHA", x=12.5, y=45.0, z=120.8, signal_dbm=-68.2)
    packet_b = node.ingest_telemetry("UAV-BRAVO", x=-34.2, y=88.1, z=210.5, signal_dbm=-74.5)
    
    dist_a = node.calculate_distance(packet_a.origin)
    dist_b = node.calculate_distance(packet_b.origin)
    
    print(f"[✓] Node UAV-ALPHA distance from origin: {dist_a:.3f} m | Neg Volume: {packet_a.neg_volume_block:.3f}")
    print(f"[✓] Node UAV-BRAVO distance from origin: {dist_b:.3f} m | Neg Volume: {packet_b.neg_volume_block:.3f}")
    
    print("\n[+] Exporting State Manifest:")
    print(node.export_inventory_state())

if __name__ == "__main__":
    asyncio.run(main())
