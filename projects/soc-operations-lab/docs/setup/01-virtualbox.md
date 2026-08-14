# 01 — VirtualBox

## Components

The SOC HomeLab uses three virtual machines: Kali Linux, Ubuntu with Wazuh Manager, and a Windows 11 endpoint. VirtualBox provides three logical adapters per role where applicable: MANAGEMENT, ATTACK/LAB, and NAT/INTERNET.

## Reproducibility Criteria

1. Create the three VMs.
2. Assign adapters to the three networks documented in [networking](06-networking.md).
3. Confirm IP addresses before testing detections.
4. Run scenarios only from ATTACK/LAB against SOC HomeLab assets.

VM exports, their sizes, exact ISO versions, and snapshots are not yet part of the public material. They must be recorded during a future clean rebuild before a complete step-by-step procedure can be claimed.
