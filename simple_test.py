import sys
import pandas as pd

print("🧪 Test simple de la plateforme")
print("Python version:", sys.version)
print("Pandas version:", pd.__version__)

try:
    from python_analytics.modules.performance_analyzer import FootballMetrics
    print("✅ FootballMetrics importé")
    
    # Test simple
    metrics = FootballMetrics()
    print("✅ Instance créée")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("Test terminé")
