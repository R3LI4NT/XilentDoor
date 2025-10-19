import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import subprocess
import sys
import os
from datetime import datetime
import re

class NetcatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XilentShell - GUI")
        self.root.geometry("1000x680")
        self.root.configure(bg='#2b2b2b')
        self.root.resizable(False, False)
        
        # Variables de estado
        self.server_socket = None
        self.client_socket = None
        self.is_listening = False
        self.current_process = None
        self.client_threads = []  # Lista para mantener los hilos de clientes
        self.active_clients = {}  # Diccionario para clientes activos
        
        self.setup_gui()
        
    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        title_label = ttk.Label(main_frame, 
                               text="XilentShell", 
                               font=('Arial', 20, 'bold'),
                               foreground="#0400ff")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        config_frame = ttk.LabelFrame(main_frame, text="Configuración del Servidor", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(config_frame, text="Puerto:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.port_var = tk.StringVar(value="4444")
        self.port_entry = ttk.Entry(config_frame, textvariable=self.port_var, width=10)
        self.port_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        self.start_btn = ttk.Button(config_frame, text="Iniciar Servidor", command=self.start_server)
        self.start_btn.grid(row=0, column=2, padx=(0, 5))
        
        self.stop_btn = ttk.Button(config_frame, text="Detener Servidor", command=self.stop_server, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=3, padx=(0, 5))
        
        status_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="Servidor detenido")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground='#ff5555')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        terminal_frame = ttk.LabelFrame(main_frame, text="Terminal - Salida del Shell", padding="10")
        terminal_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        terminal_frame.columnconfigure(0, weight=1)
        terminal_frame.rowconfigure(0, weight=1)
        
        self.terminal_output = scrolledtext.ScrolledText(
            terminal_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=20,
            bg='#1e1e1e',
            fg='#00ff00',
            insertbackground='white',
            font=('Consolas', 10)
        )
        self.terminal_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.terminal_output.config(state=tk.DISABLED)
        
        input_frame = ttk.Frame(terminal_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Label(input_frame, text="Comando:").grid(row=0, column=0, sticky=tk.W)
        self.cmd_var = tk.StringVar()
        self.cmd_entry = ttk.Entry(input_frame, textvariable=self.cmd_var, width=50)
        self.cmd_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        self.cmd_entry.bind('<Return>', self.execute_command)
        
        self.send_btn = ttk.Button(input_frame, text="Ejecutar", command=self.execute_command, state=tk.DISABLED)
        self.send_btn.grid(row=0, column=2)
        
        conn_frame = ttk.LabelFrame(main_frame, text="Conexiones Activas", padding="10")
        conn_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        conn_frame.columnconfigure(0, weight=1)
        
        columns = ('address', 'status', 'timestamp')
        self.conn_tree = ttk.Treeview(conn_frame, columns=columns, show='headings', height=4)
        self.conn_tree.heading('address', text='Dirección')
        self.conn_tree.heading('status', text='Estado')
        self.conn_tree.heading('timestamp', text='Hora de Conexión')
        
        self.conn_tree.column('address', width=200)
        self.conn_tree.column('status', width=100)
        self.conn_tree.column('timestamp', width=150)
        
        self.conn_tree.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        scrollbar = ttk.Scrollbar(conn_frame, orient=tk.VERTICAL, command=self.conn_tree.yview)
        self.conn_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        btn_frame = ttk.Frame(conn_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky=tk.E, pady=(5, 0))
        
        self.disconnect_btn = ttk.Button(btn_frame, text="Desconectar Cliente", 
                                       command=self.disconnect_client, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        footer_label = ttk.Label(main_frame, 
                                text="Developer: @R3LI4NT",
                                foreground="#ff0000",
                                font=('Arial', 8, 'bold'))
        footer_label.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
    def log_message(self, message):
        self.terminal_output.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.terminal_output.insert(tk.END, f"[{timestamp}] {message}\n")
        self.terminal_output.see(tk.END)
        self.terminal_output.config(state=tk.DISABLED)
    
    def update_status(self, message, color='#00ff00'):
        self.status_var.set(message)
        self.status_label.configure(foreground=color)
    
    def start_server(self):
        try:
            port = int(self.port_var.get())
            if port < 1 or port > 65535:
                messagebox.showerror("Error", "Puerto inválido. Debe estar entre 1 y 65535")
                return
            
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', port))
            self.server_socket.listen(5)
            
            self.is_listening = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.port_entry.config(state=tk.DISABLED)
            
            self.log_message(f"Servidor iniciado en puerto {port}")
            self.update_status(f"Escuchando en puerto {port}")
            
            self.listener_thread = threading.Thread(target=self.accept_connections, daemon=True)
            self.listener_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el servidor: {str(e)}")
    
    def stop_server(self):
        self.is_listening = False
        
        for client_addr, client_info in self.active_clients.items():
            try:
                client_info['socket'].close()
            except:
                pass
        
        try:
            if self.server_socket:
                self.server_socket.close()
        except:
            pass
        
        self.active_clients.clear()
        self.client_threads.clear()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.DISABLED)
        
        self.log_message("Servidor detenido")
        self.update_status("Servidor detenido", '#ff5555')
        self.conn_tree.delete(*self.conn_tree.get_children())
    
    def accept_connections(self):
        while self.is_listening:
            try:
                client_socket, client_address = self.server_socket.accept()
                
                client_id = f"{client_address[0]}:{client_address[1]}"
                self.active_clients[client_id] = {
                    'socket': client_socket,
                    'address': client_address,
                    'buffer': '',
                    'ready_for_commands': False  
                }
                
                self.root.after(0, self.handle_new_connection, client_address, client_socket)
                
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_address),
                    daemon=True
                )
                self.client_threads.append(client_thread)
                client_thread.start()
                
            except OSError:
                break  
            except Exception as e:
                self.log_message(f"Error aceptando conexión: {str(e)}")
    
    def handle_new_connection(self, client_address, client_socket):
        """Maneja una nueva conexión en el UI"""
        self.client_socket = client_socket
        self.log_message(f"Conexión establecida desde {client_address[0]}:{client_address[1]}")
        self.send_btn.config(state=tk.NORMAL)
        self.disconnect_btn.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.conn_tree.insert('', 'end', values=(
            f"{client_address[0]}:{client_address[1]}",
            "Conectado",
            timestamp
        ))
    
    def handle_client(self, client_socket, client_address):
        """Maneja la comunicación con el cliente en un hilo separado"""
        try:
            client_socket.settimeout(1.0)
            
            client_id = f"{client_address[0]}:{client_address[1]}"
            
            banner_received = False
            while not banner_received and self.is_listening and client_socket.fileno() != -1:
                try:
                    data = client_socket.recv(4096).decode('utf-8', errors='ignore')
                    if data:
                        banner_received = True
                        self.log_message(f"Banner de conexión recibido: {data.strip()}")
                        self.active_clients[client_id]['buffer'] = ''
                        self.active_clients[client_id]['ready_for_commands'] = True
                        client_socket.sendall(b"\r\nShell> ")
                except socket.timeout:
                    continue
            
            while self.is_listening and client_socket.fileno() != -1:
                try:
                    # Recibir datos del cliente
                    data = client_socket.recv(4096).decode('utf-8', errors='ignore')
                    
                    if not data:
                        self.log_message(f"Cliente {client_address[0]} envió datos vacíos, desconectando...")
                        break
                    
                    if self.active_clients[client_id]['ready_for_commands']:
                        self.active_clients[client_id]['buffer'] += data
                        
                        buffer_content = self.active_clients[client_id]['buffer']
                        lines = buffer_content.split('\n')
                        
                        for line in lines[:-1]:
                            line = line.strip()
                            if line:  
                                if self.is_error_message(line):
                                    continue
                                    
                                self.process_client_command(client_socket, client_address, line)
                        
                        self.active_clients[client_id]['buffer'] = lines[-1] if lines else ''
                                
                except socket.timeout:
                    continue
                except (ConnectionResetError, BrokenPipeError):
                    self.log_message(f"Conexión con {client_address[0]} fue resetada")
                    break
                except Exception as e:
                    self.log_message(f"Error con cliente {client_address}: {str(e)}")
                    break
                    
        except Exception as e:
            self.log_message(f"Error general con cliente {client_address}: {str(e)}")
        finally:
            try:
                client_socket.close()
            except:
                pass
            client_id = f"{client_address[0]}:{client_address[1]}"
            if client_id in self.active_clients:
                del self.active_clients[client_id]
            self.root.after(0, self.handle_client_disconnect, client_address)
    
    def is_error_message(self, line):
        error_patterns = [
            r'.*no se reconoce como un comando interno o externo.*',
            r'.*programa o archivo por lotes ejecutable.*',
            r'.*La sintaxis del comando no es correcta.*',
            r'.*El nombre de archivo, el nombre de directorio o la sintaxis de la etiqueta del volumen no son correctos.*'
        ]
        
        line_lower = line.lower()
        for pattern in error_patterns:
            if re.match(pattern, line_lower, re.IGNORECASE):
                return True
        return False
    
    def process_client_command(self, client_socket, client_address, command):
        self.log_message(f"Comando recibido de {client_address[0]}: {command}")
        
        if command.lower() == 'exit':
            client_socket.sendall(b"\r\nDesconectando...\r\n")
            self.log_message(f"Cliente {client_address[0]} solicitó desconexión")
            return False
        
        result = self.execute_system_command(command)
        client_socket.sendall(result.encode('utf-8'))
        client_socket.sendall(b"\r\nShell> ")
        
        return True
    
    def handle_client_disconnect(self, client_address):
        self.log_message(f"Cliente {client_address[0]}:{client_address[1]} desconectado")
        
        if self.client_socket and hasattr(self.client_socket, 'getpeername'):
            try:
                if self.client_socket.getpeername() == client_address:
                    self.send_btn.config(state=tk.DISABLED)
                    self.disconnect_btn.config(state=tk.DISABLED)
                    self.client_socket = None
            except:
                self.send_btn.config(state=tk.DISABLED)
                self.disconnect_btn.config(state=tk.DISABLED)
                self.client_socket = None
        
        for item in self.conn_tree.get_children():
            if self.conn_tree.item(item, 'values')[0].startswith(client_address[0]):
                self.conn_tree.delete(item)
                break
    
    def execute_system_command(self, command):
        try:
            clean_command = command.strip()
            
            result = subprocess.run(
                clean_command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30,
                cwd="C:\\",
                encoding='utf-8',
                errors='ignore'
            )
            
            output = result.stdout 
            if result.stderr:
                output += "\r\n" + result.stderr
            if not output:
                output = "Comando ejecutado exitosamente (sin salida visible)\r\n"
                
            return output + "\r\n"
            
        except subprocess.TimeoutExpired:
            return "Error: Timeout (30 segundos)\r\n"
        except Exception as e:
            return f"Error ejecutando comando: {str(e)}\r\n"
    
    def execute_command(self, event=None):
        """Ejecuta un comando desde la GUI"""
        command = self.cmd_var.get().strip()
        if not command or not self.client_socket:
            return
        
        try:
            self.client_socket.sendall((command + "\n").encode('utf-8'))
            self.log_message(f"Comando enviado: {command}")
            self.cmd_var.set("")
            
        except Exception as e:
            self.log_message(f"Error enviando comando: {str(e)}")
            self.handle_client_disconnect(('Desconocido', 0))
    
    def disconnect_client(self):
        if self.client_socket:
            try:
                self.client_socket.sendall(b"exit\n")
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
            self.send_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = NetcatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()