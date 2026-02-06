from typing import Dict, Any

class Worker:
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Worker.process is not implemented yet")
