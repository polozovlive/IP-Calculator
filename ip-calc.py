import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress


def calculate():
    ip = entry_ip.get().strip()
    mask_selection = combo_mask.get()

    try:
        prefix = mask_selection.split(" - ")[0]
        network = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)

        net_addr = network.network_address
        broadcast = network.broadcast_address
        netmask = network.netmask

        hosts = list(network.hosts())

        if hosts:
            host_min = hosts[0]
            host_max = hosts[-1]
            host_count = len(hosts)
        else:
            host_min = "-"
            host_max = "-"
            host_count = 0

        result = (
            f"Адрес: {ip}\n"
            f"Bitmask: {prefix}\n"
            f"Netmask: {netmask}\n"
            f"Network: {net_addr}\n"
            f"Broadcast: {broadcast}\n"
            f"Hostmin: {host_min}\n"
            f"Hostmax: {host_max}\n"
            f"Hosts: {host_count}"
        )

        result_text.set(result)

    except Exception:
        messagebox.showerror("Ошибка", "Неверный IP!\nПример: 192.168.0.1")


def copy_result():
    result = result_text.get()

    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        root.update()  # важно для некоторых систем
        messagebox.showinfo("Готово", "Результат скопирован в буфер обмена")
    else:
        messagebox.showwarning("Внимание", "Сначала выполните расчет")


# --- GUI ---
root = tk.Tk()
root.title("IP Calculator")
root.geometry("380x380")

tk.Label(root, text="IP адрес:").pack(pady=5)
entry_ip = tk.Entry(root, width=30)
entry_ip.pack()

tk.Label(root, text="Выберите маску:").pack(pady=5)

mask_list = []
for i in range(32, -1, -1):
    netmask = ipaddress.IPv4Network(f"0.0.0.0/{i}").netmask
    mask_list.append(f"{i} - {netmask}")

combo_mask = ttk.Combobox(root, values=mask_list, width=30)
combo_mask.pack()
combo_mask.current(8)  # /24

tk.Button(root, text="Рассчитать", command=calculate).pack(pady=10)

# 🔥 Кнопка копирования
tk.Button(root, text="Скопировать результат", command=copy_result).pack(pady=5)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", font=("Courier", 10))
result_label.pack(pady=10)

root.mainloop()