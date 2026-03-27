#!/usr/bin/env python3
"""
Network Traffic Collector - Simulates NetFlow/IPFIX data collection
Network Engineer: Israr Sadaq
"""

import time
import random
import threading
import json
import logging
from datetime import datetime
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TrafficCollector:
    """Collects network traffic data from simulated devices"""
    
    def __init__(self):
        self.traffic_data = defaultdict(lambda: {
            "bytes_in": 0,
            "bytes_out": 0,
            "packets_in": 0,
            "packets_out": 0,
            "applications": defaultdict(int),
            "top_talkers": defaultdict(int)
        })
        self.running = False
        self.thread = None
        
        # Define devices
        self.devices = [
            {"name": "Core-SW-01", "ip": "10.10.10.1", "type": "core"},
            {"name": "Dist-SW-F1", "ip": "10.10.10.11", "type": "distribution"},
            {"name": "Dist-SW-F2", "ip": "10.10.10.12", "type": "distribution"},
            {"name": "Dist-SW-F3", "ip": "10.10.10.13", "type": "distribution"},
            {"name": "Access-F1-01", "ip": "10.10.20.1", "type": "access"},
            {"name": "Access-F2-01", "ip": "10.10.20.2", "type": "access"},
            {"name": "Access-F3-01", "ip": "10.10.20.3", "type": "access"},
            {"name": "Firewall-01", "ip": "10.10.10.254", "type": "firewall"}
        ]
        
        # Define applications and their typical bandwidth
        self.applications = {
            "HTTP": {"port": 80, "bandwidth_range": (0.5, 5), "color": "#22c55e"},
            "HTTPS": {"port": 443, "bandwidth_range": (1, 10), "color": "#3b82f6"},
            "VoIP": {"port": 5060, "bandwidth_range": (0.1, 1), "color": "#eab308"},
            "Video": {"port": 1935, "bandwidth_range": (2, 15), "color": "#ef4444"},
            "File Transfer": {"port": 20, "bandwidth_range": (5, 50), "color": "#8b5cf6"},
            "DNS": {"port": 53, "bandwidth_range": (0.01, 0.5), "color": "#6b7280"},
            "Email": {"port": 25, "bandwidth_range": (0.1, 2), "color": "#ec489a"},
            "Database": {"port": 3306, "bandwidth_range": (1, 20), "color": "#14b8a6"},
            "VPN": {"port": 1194, "bandwidth_range": (0.5, 10), "color": "#f97316"},
            "Streaming": {"port": 554, "bandwidth_range": (3, 25), "color": "#dc2626"}
        }
        
        # Define top talkers (users)
        self.users = [
            "192.168.1.10 (CEO)", "192.168.1.20 (IT Manager)", "192.168.1.30 (Network Admin)",
            "192.168.1.40 (Finance)", "192.168.1.50 (Marketing)", "192.168.1.60 (Sales)",
            "192.168.1.70 (HR)", "192.168.1.80 (Development)", "192.168.1.90 (Student Lab)",
            "192.168.1.100 (Guest WiFi)"
        ]
    
    def start(self):
        """Start traffic collection"""
        self.running = True
        self.thread = threading.Thread(target=self._collect_traffic)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Traffic collector started")
    
    def stop(self):
        """Stop traffic collection"""
        self.running = False
        logger.info("Traffic collector stopped")
    
    def _collect_traffic(self):
        """Simulate traffic collection"""
        while self.running:
            for device in self.devices:
                # Generate random traffic data
                total_bandwidth = random.uniform(10, 500)  # Mbps
                app_data = {}
                
                # Distribute bandwidth among applications
                remaining = total_bandwidth
                for app_name, app_info in list(self.applications.items()):
                    if remaining <= 0:
                        break
                    app_bandwidth = random.uniform(
                        app_info["bandwidth_range"][0],
                        min(app_info["bandwidth_range"][1], remaining)
                    )
                    app_data[app_name] = app_bandwidth
                    remaining -= app_bandwidth
                
                # Generate top talkers
                talkers = {}
                for user in random.sample(self.users, random.randint(3, 8)):
                    talkers[user] = random.uniform(1, 50)
                
                # Store data
                self.traffic_data[device["name"]] = {
                    "device_name": device["name"],
                    "device_ip": device["ip"],
                    "device_type": device["type"],
                    "timestamp": datetime.now().isoformat(),
                    "total_bandwidth_mbps": round(total_bandwidth, 2),
                    "applications": app_data,
                    "top_talkers": talkers,
                    "inbound_mbps": round(total_bandwidth * random.uniform(0.4, 0.6), 2),
                    "outbound_mbps": round(total_bandwidth * random.uniform(0.4, 0.6), 2),
                    "packet_rate_pps": random.randint(1000, 50000),
                    "utilization_percent": round(total_bandwidth / 1000 * 100, 1)  # Assuming 1Gbps link
                }
            
            time.sleep(5)  # Collect every 5 seconds
    
    def get_all_traffic(self):
        """Get current traffic data for all devices"""
        return dict(self.traffic_data)
    
    def get_device_traffic(self, device_name):
        """Get traffic data for specific device"""
        return self.traffic_data.get(device_name, {})
    
    def get_top_talkers(self, limit=10):
        """Get top bandwidth consumers"""
        all_talkers = defaultdict(float)
        for device_data in self.traffic_data.values():
            for talker, bandwidth in device_data.get("top_talkers", {}).items():
                all_talkers[talker] += bandwidth
        
        sorted_talkers = sorted(all_talkers.items(), key=lambda x: x[1], reverse=True)
        return sorted_talkers[:limit]
    
    def get_application_breakdown(self):
        """Get bandwidth breakdown by application"""
        app_total = defaultdict(float)
        for device_data in self.traffic_data.values():
            for app, bandwidth in device_data.get("applications", {}).items():
                app_total[app] += bandwidth
        
        return dict(app_total)
    
    def get_total_bandwidth(self):
        """Get total network bandwidth usage"""
        total = 0
        for device_data in self.traffic_data.values():
            total += device_data.get("total_bandwidth_mbps", 0)
        return round(total, 2)
    
    def get_device_summary(self):
        """Get summary of all devices"""
        summary = []
        for device_name, data in self.traffic_data.items():
            summary.append({
                "name": device_name,
                "type": data["device_type"],
                "ip": data["device_ip"],
                "bandwidth_mbps": data["total_bandwidth_mbps"],
                "utilization": data["utilization_percent"],
                "inbound": data["inbound_mbps"],
                "outbound": data["outbound_mbps"]
            })
        return summary


class BandwidthManager:
    """Manages bandwidth and applies QoS policies"""
    
    def __init__(self, threshold_high=80, threshold_critical=95):
        self.threshold_high = threshold_high  # 80% utilization
        self.threshold_critical = threshold_critical  # 95% utilization
        self.alerts = []
        self.qos_policies = {
            "priority": ["VoIP", "Video"],
            "normal": ["HTTP", "HTTPS", "Email", "DNS"],
            "limited": ["Streaming", "File Transfer", "VPN"]
        }
    
    def check_bandwidth(self, traffic_data):
        """Check bandwidth usage and generate alerts"""
        alerts = []
        for device_name, data in traffic_data.items():
            util = data.get("utilization_percent", 0)
            
            if util >= self.threshold_critical:
                alerts.append({
                    "severity": "critical",
                    "device": device_name,
                    "message": f"Bandwidth utilization at {util}% - CRITICAL!",
                    "action": "Apply rate limiting immediately",
                    "timestamp": datetime.now().isoformat()
                })
            elif util >= self.threshold_high:
                alerts.append({
                    "severity": "warning",
                    "device": device_name,
                    "message": f"Bandwidth utilization at {util}% - High usage",
                    "action": "Consider QoS policies",
                    "timestamp": datetime.now().isoformat()
                })
        
        return alerts
    
    def apply_qos(self, traffic_data):
        """Apply QoS policies based on current usage"""
        recommendations = []
        app_breakdown = {}
        
        for data in traffic_data.values():
            for app, bandwidth in data.get("applications", {}).items():
                app_breakdown[app] = app_breakdown.get(app, 0) + bandwidth
        
        # Check if streaming is using too much bandwidth
        streaming_bandwidth = app_breakdown.get("Streaming", 0)
        if streaming_bandwidth > 100:  # 100 Mbps
            recommendations.append({
                "action": "Throttle Streaming",
                "details": f"Streaming using {streaming_bandwidth:.1f} Mbps",
                "policy": "Limit to 50 Mbps during business hours"
            })
        
        # Check if VoIP has enough bandwidth
        voip_bandwidth = app_breakdown.get("VoIP", 0)
        if voip_bandwidth < 10:  # Reserve at least 10 Mbps for VoIP
            recommendations.append({
                "action": "Increase VoIP Priority",
                "details": f"VoIP only {voip_bandwidth:.1f} Mbps",
                "policy": "Reserve minimum 10 Mbps for VoIP"
            })
        
        return recommendations
    
    def get_qos_policy(self, application):
        """Get QoS policy for specific application"""
        if application in self.qos_policies["priority"]:
            return "High Priority (EF)"
        elif application in self.qos_policies["normal"]:
            return "Normal (AF)"
        elif application in self.qos_policies["limited"]:
            return "Limited (BE)"
        return "Default"


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("NETWORK TRAFFIC ANALYZER & BANDWIDTH MANAGER")
    print("Network Engineer: Israr Sadaq")
    print("="*70)
    
    collector = TrafficCollector()
    manager = BandwidthManager(threshold_high=70, threshold_critical=85)
    
    print("\n📡 Starting traffic collection...\n")
    collector.start()
    
    try:
        while True:
            time.sleep(10)
            
            print("\n" + "="*70)
            print(f"TRAFFIC REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*70)
            
            # Total bandwidth
            total_bandwidth = collector.get_total_bandwidth()
            print(f"\n📊 TOTAL NETWORK BANDWIDTH: {total_bandwidth:.2f} Mbps")
            
            # Top talkers
            print("\n🔝 TOP TALKERS:")
            top_talkers = collector.get_top_talkers(5)
            for i, (talker, bw) in enumerate(top_talkers, 1):
                print(f"   {i}. {talker}: {bw:.2f} Mbps")
            
            # Application breakdown
            print("\n📱 APPLICATION BREAKDOWN:")
            apps = collector.get_application_breakdown()
            for app, bw in sorted(apps.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   {app}: {bw:.2f} Mbps")
            
            # Device summary
            print("\n🖧 DEVICE SUMMARY:")
            devices = collector.get_device_summary()
            for d in devices[:5]:
                status = "⚠️" if d["utilization"] > 70 else "✅"
                print(f"   {status} {d['name']} ({d['type']}): {d['bandwidth_mbps']:.1f} Mbps ({d['utilization']}%)")
            
            # Check alerts
            alerts = manager.check_bandwidth(collector.get_all_traffic())
            if alerts:
                print("\n⚠️ ALERTS:")
                for alert in alerts[:3]:
                    print(f"   [{alert['severity'].upper()}] {alert['device']}: {alert['message']}")
                    print(f"      → {alert['action']}")
            
            # QoS recommendations
            qos_recs = manager.apply_qos(collector.get_all_traffic())
            if qos_recs:
                print("\n🎯 QoS RECOMMENDATIONS:")
                for rec in qos_recs:
                    print(f"   → {rec['action']}: {rec['details']}")
                    print(f"      Policy: {rec['policy']}")
            
            print("\n" + "-"*70)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping traffic collector...")
        collector.stop()
        print("✅ Done!")


if __name__ == "__main__":
    main()