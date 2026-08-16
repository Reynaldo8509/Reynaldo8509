# Reparación de conectividad Wazuh — 2026-08-15

## Causa

VirtualBox ya tenía conectada la NIC 3 del manager a `vboxnet1`, pero Ubuntu la
exponía como `enp0s9` sin gestión de Netplan y en estado DOWN. Por ello
`192.168.57.10` no respondía ni aceptaba SSH. La red ATTACK/LAB (`enp0s8`,
`192.168.56.10`) seguía operativa.

## Cambio aplicado

Se creó, antes del cambio, la copia:

`/etc/netplan/50-cloud-init.yaml.bak-before-management-20260815-1945`

en el manager. En `/etc/netplan/50-cloud-init.yaml` se añadió únicamente:

```yaml
enp0s9:
  addresses:
  - "192.168.57.10/24"
```

Se validó con `netplan generate` y se aplicó con `netplan apply`. No se modificó
Wazuh ni se reinició ningún servicio o máquina virtual.

## Verificación

- `192.168.56.10`: ICMP y SSH disponibles.
- `192.168.57.10`: ICMP y TCP/22 disponibles.
- Ambas interfaces aparecen UP en el manager.
- `ssh` está `active` y `enabled`.
- `ssh wazuh` del perfil `reyam`, con `PasswordAuthentication=no`, autentica como
  `soc-admin`; por tanto usa la clave pública configurada y no una contraseña.
- La interfaz NAT del manager es `10.0.2.3/24`; `10.0.2.2` es su gateway NAT.

No se registraron ni publicaron contraseñas.
