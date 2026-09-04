import pytest
from mesh_engine import SpatialMeshEngine, Coordinate3D

def test_distance_calculation():
    node = SpatialMeshEngine(node_id="TEST-NODE", origin_x=0.0, origin_y=0.0, origin_z=0.0)
    target = Coordinate3D(x=3.0, y=4.0, z=0.0)
    assert node.calculate_distance(target) == 5.0

def test_volume_block_inversion():
    node = SpatialMeshEngine(node_id="TEST-NODE")
    neg_vol = node.process_volume_block(10.0, 5.0, 2.0)
    assert neg_vol == -100.0

def test_telemetry_ingestion():
    node = SpatialMeshEngine(node_id="TEST-NODE")
    packet = node.ingest_telemetry("NODE-A", x=1.0, y=1.0, z=1.0, signal_dbm=-50.0)
    assert packet.node_id == "NODE-A"
    assert packet.neg_volume_block == -1.0
    assert "NODE-A" in node.active_inventory
