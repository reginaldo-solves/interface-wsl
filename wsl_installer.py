"""
WSL Development Environment Installer
Automatically installs WSL and Debian distribution with user credentials
"""

import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk
import subprocess
import os
import sys
import ctypes
import threading
import queue
import re


class WSLInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WSL Development Environment Installer")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Remove the white title bar
        self.root.overrideredirect(True)
        
        # Variables to store credentials
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.distro_var = tk.StringVar(value="Debian")
        self.available_distros = []
        self.installed_distro_var = tk.StringVar(value="")
        self.installed_distros = []
        self.log_queue = queue.Queue()
        self.log_pump_job = None
        
        # Variables for window dragging
        self.offset_x = 0
        self.offset_y = 0
        
        # Configure window background
        self.root.configure(bg="#2c3e50")
        
        # Center the window on screen
        self.center_window()
        
        # Create main container with rounded effect
        self.create_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def start_drag(self, event):
        """Start dragging the window"""
        self.offset_x = event.x
        self.offset_y = event.y
    
    def do_drag(self, event):
        """Drag the window"""
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f'+{x}+{y}')
    
    def create_ui(self):
        """Create the user interface"""
        # Custom title bar
        title_bar = tk.Frame(self.root, bg="#1a252f", height=40, relief="flat")
        title_bar.pack(fill="x", side="top")
        
        # Title bar label
        title_font = font.Font(family="Segoe UI", size=10, weight="bold")
        title_label = tk.Label(
            title_bar,
            text="WSL Development Environment Installer",
            font=title_font,
            bg="#1a252f",
            fg="#ecf0f1",
            anchor="w"
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        # Close button
        close_btn = tk.Label(
            title_bar,
            text="✕",
            font=font.Font(family="Segoe UI", size=14, weight="bold"),
            bg="#1a252f",
            fg="#ecf0f1",
            cursor="hand2",
            padx=15,
            pady=5
        )
        close_btn.pack(side="right", padx=5)
        close_btn.bind("<Button-1>", lambda e: self.root.quit())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#e74c3c"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#1a252f"))
        
        # Make title bar draggable
        title_bar.bind("<Button-1>", self.start_drag)
        title_bar.bind("<B1-Motion>", self.do_drag)
        title_label.bind("<Button-1>", self.start_drag)
        title_label.bind("<B1-Motion>", self.do_drag)
        
        # Main frame with padding
        main_frame = tk.Frame(self.root, bg="#34495e", padx=40, pady=40)
        main_frame.pack(expand=True, fill="both")
        
        # Title
        title_font = font.Font(family="Segoe UI", size=20, weight="bold")
        title_label = tk.Label(
            main_frame,
            text="WSL Installer",
            font=title_font,
            bg="#34495e",
            fg="#ecf0f1"
        )
        title_label.pack(pady=(0, 30))
        
        # Username field
        self.create_input_field(main_frame, "Username:", self.username_var, False)
        
        # Password field
        self.create_input_field(main_frame, "Password:", self.password_var, True)

        # Distribution selector
        self.create_distro_selector(main_frame)

        # Installed distributions (list / delete)
        self.create_installed_distro_controls(main_frame)
        
        # Install button
        button_font = font.Font(family="Segoe UI", size=12, weight="bold")
        install_btn = tk.Button(
            main_frame,
            text="INSTALL WSL & DISTRO",
            font=button_font,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.start_installation
        )
        install_btn.pack(pady=(20, 0))
        
        # Add hover effect
        install_btn.bind("<Enter>", lambda e: install_btn.config(bg="#2980b9"))
        install_btn.bind("<Leave>", lambda e: install_btn.config(bg="#3498db"))

    def create_installed_distro_controls(self, parent):
        field_frame = tk.Frame(parent, bg="#34495e")
        self.installed_frame = field_frame
        # Initially hidden; will be shown if we detect installed distros

        label_font = font.Font(family="Segoe UI", size=11, weight="bold")
        label = tk.Label(
            field_frame,
            text="Installed distros:",
            font=label_font,
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 5))

        row = tk.Frame(field_frame, bg="#34495e")
        row.pack(fill="x")

        self.installed_combo = ttk.Combobox(
            row,
            textvariable=self.installed_distro_var,
            state="readonly",
            style="WSL.TCombobox"
        )
        self.installed_combo.pack(side="left", fill="x", expand=True)

        list_btn = tk.Button(
            row,
            text="List",
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            activeforeground="white",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.list_installed_distros
        )
        list_btn.pack(side="left", padx=(10, 0))

        del_btn = tk.Button(
            row,
            text="Delete",
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.delete_selected_distro
        )
        del_btn.pack(side="left", padx=(10, 0))

        self.installed_combo["values"] = []
        self.root.after(300, self.refresh_installed_distros)

    def create_distro_selector(self, parent):
        field_frame = tk.Frame(parent, bg="#34495e")
        field_frame.pack(pady=10, fill="x")

        label_font = font.Font(family="Segoe UI", size=11, weight="bold")
        label = tk.Label(
            field_frame,
            text="Distribution:",
            font=label_font,
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 5))

        combo_style = ttk.Style()
        try:
            combo_style.theme_use("clam")
        except:
            pass
        combo_style.configure(
            "WSL.TCombobox",
            fieldbackground="#2c3e50",
            background="#2c3e50",
            foreground="#ecf0f1"
        )

        self.distro_combo = ttk.Combobox(
            field_frame,
            textvariable=self.distro_var,
            state="readonly",
            style="WSL.TCombobox"
        )
        self.distro_combo.pack(fill="x", ipady=3)

        self.distro_combo["values"] = ["Debian"]
        self.root.after(200, self.refresh_distros)

    def refresh_distros(self):
        distros = self.get_online_distributions()
        if not distros:
            err = getattr(self, "last_online_list_error", "").strip()
            if err:
                messagebox.showwarning("WSL", f"Could not list online distributions.\n\n{err}")
            distros = ["Debian"]
        self.available_distros = distros
        if hasattr(self, "distro_combo"):
            self.distro_combo["values"] = distros
            current = self.distro_var.get().strip()
            if current not in distros:
                self.distro_var.set(distros[0])

    def refresh_installed_distros(self):
        distros = self.get_installed_distributions()
        self.installed_distros = distros
        if hasattr(self, "installed_combo"):
            self.installed_combo["values"] = distros
            current = self.installed_distro_var.get().strip()
            if distros and current not in distros:
                self.installed_distro_var.set(distros[0])
            if not distros:
                self.installed_distro_var.set("")

        # Show/hide installed distros frame
        if hasattr(self, "installed_frame"):
            if distros:
                if not self.installed_frame.winfo_ismapped():
                    self.installed_frame.pack(pady=(10, 0), fill="x")
            else:
                if self.installed_frame.winfo_ismapped():
                    self.installed_frame.pack_forget()

    def get_installed_distributions(self):
        try:
            result = subprocess.run(
                ["wsl.exe", "--list", "--quiet"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=30
            )
            out = self.decode_windows_output(result.stdout)
            if result.returncode != 0 or not out.strip():
                return []
            distros = []
            for ln in out.splitlines():
                name = self.clean_distro_name(ln)
                if name and name.lower() != "name" and name not in distros:
                    distros.append(name)
            return distros
        except:
            return []

    def ensure_monitor_open(self):
        if not hasattr(self, "monitor_window") or not hasattr(self, "log_text"):
            self.show_monitor_window()
            self.start_log_pump()
        try:
            self.monitor_window.lift()
        except:
            pass

    def list_installed_distros(self):
        self.ensure_monitor_open()

        worker = threading.Thread(
            target=self.list_installed_worker,
            daemon=True
        )
        worker.start()

    def list_installed_worker(self):
        self.set_status("Listing installed distributions...")
        self.log_queue.put("\n=== wsl --list ===")
        code = self.run_process_stream(["wsl.exe", "--list", "--verbose"])
        if code != 0:
            self.log_queue.put("Failed to list installed distributions.")
        self.refresh_installed_distros()
        self.set_status("Ready")

    def delete_selected_distro(self):
        distro = self.clean_distro_name(self.installed_distro_var.get())
        if not distro:
            messagebox.showwarning("WSL", "Select an installed distribution to delete.")
            return

        ok = messagebox.askyesno(
            "Confirm delete",
            f"This will unregister and delete '{distro}'.\n\nContinue?"
        )
        if not ok:
            return

        self.ensure_monitor_open()
        worker = threading.Thread(
            target=self.delete_distro_worker,
            args=(distro,),
            daemon=True
        )
        worker.start()

    def delete_distro_worker(self, distro):
        distro = self.clean_distro_name(distro)
        self.set_status(f"Deleting {distro}...")
        self.log_queue.put(f"\n=== wsl --unregister {distro} ===")
        code = self.run_process_stream(["wsl.exe", "--unregister", distro])
        if code == 0:
            self.log_queue.put(f"Deleted '{distro}'.")
        else:
            self.log_queue.put(f"Failed to delete '{distro}'.")
        self.refresh_installed_distros()
        self.set_status("Ready")

    def get_online_distributions(self):
        try:
            result = subprocess.run(
                ["wsl.exe", "--list", "--online"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=120
            )

            stdout = self.decode_windows_output(result.stdout)
            if result.returncode != 0 or not stdout.strip():
                # Fallback: run via PowerShell (some environments behave better with a shell host)
                ps = subprocess.run(
                    [
                        "powershell",
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-Command",
                        "wsl.exe --list --online"
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=120
                )
                ps_out = self.decode_windows_output(ps.stdout)
                if ps.returncode == 0 and ps_out.strip():
                    stdout = ps_out
                else:
                    # Keep some diagnostics for troubleshooting
                    self.last_online_list_error = (stdout or "") or (ps_out or "")
                    return []

            lines = [ln.rstrip() for ln in stdout.splitlines()]
            distros = []
            in_table = False
            for ln in lines:
                if not ln.strip():
                    continue

                stripped = ln.strip()

                # Some builds don't include a dashed separator. Start table after header.
                # Example header (pt-BR): "NAME  FRIENDLY NAME"
                upper = stripped.upper()
                if not in_table and "NAME" in upper and "FRIENDLY" in upper:
                    in_table = True
                    continue

                # Locale-independent: table begins after the dashed separator line
                if not in_table and len(stripped) >= 3 and set(stripped) <= set("-"):
                    in_table = True
                    continue

                if in_table:
                    # First column is distro name
                    parts = stripped.split()
                    if not parts:
                        continue
                    name = self.clean_distro_name(parts[0])
                    if name and name.lower() != "name" and name not in distros:
                        distros.append(name)

            # Extra fallback: some locales/versions may omit the header but still print rows.
            if not distros:
                for ln in lines:
                    s = ln.strip()
                    if not s:
                        continue
                    up = s.upper()
                    if up.startswith("A SEGUIR") or up.startswith("INSTAL"):
                        continue
                    if "WSL.EXE" in up:
                        continue
                    if "NAME" in up and "FRIENDLY" in up:
                        continue
                    parts = s.split()
                    if parts:
                        cand = self.clean_distro_name(parts[0])
                        if cand and cand.lower() != "name" and cand not in distros:
                            distros.append(cand)

            return distros
        except:
            return []

    def decode_windows_output(self, data):
        if data is None:
            return ""
        if isinstance(data, str):
            return data
        try:
            if b"\x00" in data:
                return data.decode("utf-16-le", errors="ignore")
            return data.decode("mbcs", errors="ignore")
        except Exception:
            try:
                return data.decode(errors="ignore")
            except Exception:
                return ""

    def clean_distro_name(self, name):
        if name is None:
            return ""
        name = str(name).replace("\x00", "")
        name = re.sub(r"[\r\n\t]", " ", name)
        return name.strip()
        
    def create_input_field(self, parent, label_text, variable, is_password):
        """Create a styled input field"""
        # Container for each field
        field_frame = tk.Frame(parent, bg="#34495e")
        field_frame.pack(pady=10, fill="x")
        
        # Label
        label_font = font.Font(family="Segoe UI", size=11, weight="bold")
        label = tk.Label(
            field_frame,
            text=label_text,
            font=label_font,
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 5))
        
        # Entry field with rounded appearance
        entry_font = font.Font(family="Segoe UI", size=11)
        entry = tk.Entry(
            field_frame,
            textvariable=variable,
            font=entry_font,
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            bd=0,
            relief="flat",
            show="●" if is_password else ""
        )
        entry.pack(fill="x", ipady=8, ipadx=10)
        
        # Add focus effects
        entry.bind("<FocusIn>", lambda e: entry.config(bg="#1a252f"))
        entry.bind("<FocusOut>", lambda e: entry.config(bg="#2c3e50"))
        
    def check_admin(self):
        """Check if script is running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def save_to_env(self, distro_name):
        """Save credentials to .env file (per-distro keys, non-destructive)"""
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        distro_key = self.env_key_from_distro(distro_name)
        user_key = f"{distro_key}_USERNAME"
        pass_key = f"{distro_key}_PASSWORD"
        updates = {
            user_key: self.username_var.get(),
            pass_key: self.password_var.get()
        }

        existing = {}
        raw_lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_lines = f.read().splitlines()

            for ln in raw_lines:
                if not ln.strip() or ln.lstrip().startswith("#"):
                    continue
                if "=" not in ln:
                    continue
                k, v = ln.split("=", 1)
                k = k.strip()
                if k:
                    existing[k] = v

        # Apply updates
        existing.update(updates)

        # Rebuild file preserving original ordering as much as possible
        written_keys = set()
        out_lines = []
        for ln in raw_lines:
            if not ln.strip() or ln.lstrip().startswith("#") or "=" not in ln:
                out_lines.append(ln)
                continue
            k, _ = ln.split("=", 1)
            k = k.strip()
            if k in existing:
                out_lines.append(f"{k}={existing[k]}")
                written_keys.add(k)
            else:
                out_lines.append(ln)

        # Append any new keys that weren't present
        for k in (user_key, pass_key):
            if k not in written_keys:
                out_lines.append(f"{k}={existing[k]}")

        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines).rstrip("\n") + "\n")

        return env_path, user_key, pass_key

    def env_key_from_distro(self, distro_name):
        name = self.clean_distro_name(distro_name).upper()
        name = re.sub(r"[^A-Z0-9]", "_", name)
        name = re.sub(r"_+", "_", name).strip("_")
        return name or "WSL"
    
    def check_wsl_installed(self):
        """Check if WSL is already installed"""
        try:
            result = subprocess.run(
                ["wsl", "--status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def install_wsl(self):
        """Install WSL using PowerShell"""
        code = self.run_process_stream([
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "wsl --install --no-distribution"
        ])
        if code != 0:
            self.show_error("Failed to install WSL")
            return False
        return True
    
    def install_distribution(self, distro_name):
        """Install selected WSL distribution"""
        distro_name = self.clean_distro_name(distro_name)
        if not distro_name:
            self.last_process_output = "Invalid distribution name."
            self.log_queue.put(self.last_process_output)
            return False
        code = self.run_process_stream([
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"wsl --install -d \"{distro_name}\" --no-launch"
        ])
        if code != 0:
            self.show_error(f"Failed to install {distro_name}")
            return False
        return True
    
    def configure_distribution(self, distro_name):
        """Configure WSL distribution with user credentials"""
        distro_name = self.clean_distro_name(distro_name)
        if not distro_name:
            messagebox.showerror("Error", "Invalid distribution name.")
            return False
        username = self.username_var.get()
        password = self.password_var.get()
        
        try:
            bash_username = self.bash_single_quote(username)
            bash_password = self.bash_single_quote(password)

            # Create the user and add to sudo group (non-interactive)
            # - useradd may fail if user already exists; we treat that as ok.
            bash_cmd = (
                f"set -e; "
                f"(id -u {bash_username} >/dev/null 2>&1 || useradd -m -s /bin/bash {bash_username}); "
                f"echo {bash_username}:{bash_password} | chpasswd; "
                f"usermod -aG sudo {bash_username}; "
                f"true"
            )

            code = self.run_process_stream([
                "wsl",
                "-d",
                distro_name,
                "-u",
                "root",
                "--",
                "bash",
                "-lc",
                bash_cmd
            ])
            if code != 0:
                raise RuntimeError("WSL configuration command failed")

            # Set default user (so next launch uses this user and avoids the prompt)
            code = self.run_process_stream([
                "wsl",
                "--manage",
                distro_name,
                "--set-default-user",
                username
            ])
            if code != 0:
                raise RuntimeError("Failed to set default user")

            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to configure {distro_name}: {str(e)}")
            return False

    def bash_single_quote(self, s):
        # Safely single-quote for bash: ' -> '\''
        return "'" + s.replace("'", "'\\''") + "'"

    def run_process_stream(self, args):
        self.last_process_output = ""
        try:
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=False
            )
            out_lines = []
            if proc.stdout is not None:
                while True:
                    line_bytes = proc.stdout.readline()
                    if not line_bytes:
                        break
                    # Decode using the same helper we use for wsl --list --online
                    line = self.decode_windows_output(line_bytes)
                    out_lines.append(line)
                    self.log_queue.put(line.rstrip("\n"))
            proc.wait()
            self.last_process_output = "".join(out_lines)
            return proc.returncode
        except Exception as e:
            self.last_process_output = str(e)
            self.log_queue.put(str(e))
            return 1

    def show_error(self, title):
        details = getattr(self, "last_process_output", "")
        if details:
            messagebox.showerror(title, details)
        else:
            messagebox.showerror(title, "An unknown error occurred.")
    
    def start_installation(self):
        """Main installation process"""
        # Validate inputs
        if not self.username_var.get() or not self.password_var.get():
            messagebox.showwarning("Warning", "Please enter both username and password!")
            return

        distro_name = self.clean_distro_name(self.distro_var.get()) or "Debian"
        
        # Check for admin privileges
        if not self.check_admin():
            messagebox.showerror(
                "Administrator Required",
                "This script requires administrator privileges.\n"
                "Please run as administrator and try again."
            )
            return
        
        # Hide main window and show progress
        self.root.withdraw()
        self.show_monitor_window()
        self.start_log_pump()

        worker = threading.Thread(
            target=self.installation_worker,
            args=(distro_name,),
            daemon=True
        )
        worker.start()

    def installation_worker(self, distro_name):
        try:
            distro_name = self.clean_distro_name(distro_name) or "Debian"
            self.log_queue.put("Checking WSL installation...")
            self.set_status("Checking WSL installation...")
            if not self.check_wsl_installed():
                self.log_queue.put("Installing WSL...")
                self.set_status("Installing WSL...")
                if not self.install_wsl():
                    self.log_queue.put("WSL installation failed.")
                    self.set_status("Installation failed")
                    self.root.after(0, lambda: self.installation_failed())
                    return
                self.root.after(0, lambda: messagebox.showinfo(
                    "Restart Required",
                    "WSL has been installed. Please restart your computer and run this script again."
                ))
                self.root.after(0, self.root.quit)
                return

            self.log_queue.put(f"Installing {distro_name} distribution...")
            self.set_status(f"Installing {distro_name} distribution...")
            if not self.install_distribution(distro_name):
                self.log_queue.put("Distribution installation failed.")
                self.set_status("Installation failed")
                self.root.after(0, lambda: self.installation_failed())
                return

            self.log_queue.put(f"Configuring {distro_name} with user credentials...")
            self.set_status(f"Configuring {distro_name}...")
            if not self.configure_distribution(distro_name):
                self.log_queue.put("Distribution configuration failed.")
                self.set_status("Installation failed")
                self.root.after(0, lambda: self.installation_failed())
                return

            self.log_queue.put("Saving credentials to .env file...")
            self.set_status("Saving credentials...")
            env_path, user_key, pass_key = self.save_to_env(distro_name)

            self.log_queue.put("Installation completed successfully.")
            self.set_status("Success")
            self.root.after(0, lambda: self.installation_succeeded(env_path, distro_name, user_key, pass_key))
        except Exception as e:
            self.log_queue.put(str(e))
            self.set_status("Installation failed")
            self.root.after(0, lambda: self.installation_failed(str(e)))

    def set_status(self, message):
        self.root.after(0, lambda: self.update_status(message))

    def update_status(self, message):
        if hasattr(self, 'status_label'):
            try:
                if self.status_label.winfo_exists():
                    self.status_label.config(text=message)
            except:
                pass

    def show_monitor_window(self):
        self.monitor_window = tk.Toplevel(self.root)
        self.monitor_window.title("WSL Installation Monitor")
        self.monitor_window.geometry("700x450")
        self.monitor_window.resizable(True, True)
        self.monitor_window.configure(bg="#34495e")

        status_font = font.Font(family="Segoe UI", size=11, weight="bold")
        self.status_label = tk.Label(
            self.monitor_window,
            text="Starting...",
            font=status_font,
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=12, pady=(12, 6))

        text_frame = tk.Frame(self.monitor_window, bg="#34495e")
        text_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.log_text = tk.Text(
            text_frame,
            bg="#1a252f",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            relief="flat",
            wrap="word"
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.insert("end", "Monitor started.\n")
        self.log_text.configure(state="disabled")

        # If user closes the monitor, stop pumping logs to avoid TclError
        self.monitor_window.protocol("WM_DELETE_WINDOW", self.on_monitor_close)

    def on_monitor_close(self):
        try:
            if self.log_pump_job is not None:
                self.root.after_cancel(self.log_pump_job)
        except:
            pass
        self.log_pump_job = None
        try:
            self.monitor_window.destroy()
        except:
            pass

    def start_log_pump(self):
        self.pump_log_queue()

    def pump_log_queue(self):
        if hasattr(self, "log_text"):
            try:
                if not self.log_text.winfo_exists():
                    self.log_pump_job = None
                    return
            except:
                self.log_pump_job = None
                return
            updated = False
            try:
                while True:
                    msg = self.log_queue.get_nowait()
                    try:
                        self.log_text.configure(state="normal")
                        self.log_text.insert("end", msg + "\n")
                        self.log_text.see("end")
                        self.log_text.configure(state="disabled")
                    except:
                        self.log_pump_job = None
                        return
                    updated = True
            except queue.Empty:
                pass
            if updated:
                try:
                    if hasattr(self, "monitor_window") and self.monitor_window.winfo_exists():
                        self.monitor_window.update_idletasks()
                except:
                    pass

        self.log_pump_job = self.root.after(100, self.pump_log_queue)

    def installation_succeeded(self, env_path, distro_name, user_key, pass_key):
        if hasattr(self, 'monitor_window'):
            try:
                self.monitor_window.destroy()
            except:
                pass
        messagebox.showinfo(
            "Success!",
            f"WSL and {distro_name} have been successfully installed!\n\n"
            f"Username: {self.username_var.get()}\n"
            f"Credentials saved to: {env_path}\n\n"
            f"Saved keys: {user_key}, {pass_key}\n\n"
            f"You can now access {distro_name} by typing 'wsl' in your terminal."
        )
        self.root.quit()
    
    def update_progress(self, message):
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
    
    def installation_failed(self, error_msg=""):
        """Handle installation failure"""
        if hasattr(self, 'monitor_window'):
            try:
                self.monitor_window.lift()
            except:
                pass
        if error_msg:
            messagebox.showerror("Installation Failed", f"An error occurred:\n{error_msg}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = WSLInstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
