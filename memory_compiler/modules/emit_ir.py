from __future__ import annotations

from ..models import IRBlock


def emit_ir(compressed_blocks: list[IRBlock]) -> dict[str, object]:
    return {
        "ir_version": "0.1",
        "context_blocks": [block.as_ir_dict() for block in compressed_blocks],
    }
