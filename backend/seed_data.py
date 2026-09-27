from models import Incident
from datetime import datetime, timedelta

def load_seed_data():
    now = datetime.now()
    
    return [
        Incident(
            id="INC-0047",
            title="prod-api-3 connection timeout",
            description="prod-api-3 is returning 502 errors. CPU is at 95%.",
            status="resolved",
            created_at=now - timedelta(days=15),
            severity="High",
            affected_services=["prod-api", "auth-service"],
            root_cause="Connection pool exhaustion in auth-service v2.3.1 due to memory leak.",
            resolution_steps=[
                "kubectl rollout restart deploy/sidecar-proxy -n prod",
                "kubectl scale deploy/auth-service --replicas=3 -n prod"
            ],
            failed_approaches=["Restarting nginx (symptoms returned in 10 mins)"]
        ),
        Incident(
            id="INC-0051",
            title="payment-service Friday outage",
            description="Payment service latency spiked to 5000ms after Friday deploy.",
            status="resolved",
            created_at=now - timedelta(days=5),
            severity="Critical",
            affected_services=["payment-service"],
            root_cause="Bad database migration locked transactions table.",
            resolution_steps=[
                "Rollback deployment to v1.42",
                "Manually kill stuck db connections"
            ],
            failed_approaches=["Scaling payment pods (database was the bottleneck)"]
        ),
        Incident(
            id="INC-0058",
            title="checkout-service timeouts",
            description="Getting intermittent 504 timeouts on checkout-service",
            status="resolved",
            created_at=now - timedelta(days=2),
            severity="High",
            affected_services=["checkout-service", "cart-service"],
            root_cause="Pod memory limits too low causing OOM kills.",
            resolution_steps=["Increased memory limits from 512Mi to 1Gi in Helm chart."],
            failed_approaches=["Restarting pod only temporarily fixed it until OOM hit again."]
        ),
        Incident(
            id="INC-0062",
            title="Active Incident: prod-api-4 high latency",
            description="prod-api-4 is returning 502 errors with intermittent CPU spikes.",
            status="active",
            created_at=now,
            severity="High",
            affected_services=["prod-api"]
        )
    ]
