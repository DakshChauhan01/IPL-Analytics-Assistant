import traceback
from app.services.orchestrator import answer_query

try:
    print("Running query...")
    res = answer_query("Rohit vs Virat", verbose=True)
    print("Success!")
    print(res)
except Exception as e:
    print("FAILED with exception:")
    traceback.print_exc()
