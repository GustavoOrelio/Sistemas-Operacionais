import os
import curses
import pycfg
from pyarch import load_binary_into_memory
from pyarch import cpu_t

class estrutura_processo:
	def __init__ (self):
		self.registradores = [0, 0, 0, 0, 0, 0, 0, 0]
		self.registrador_pc = 0
		self.estado = str("Processo pronto para executar")

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_str = ""
		self.terminal.console_print("this is the console, type the commands here\n")

	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False
		
	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
			self.console_str = self.console_str + chr(key)
			self.terminal.console_print("\r" + self.console_str)
		elif key == curses.KEY_BACKSPACE:
			self.console_str = self.console_str[:-1]
			self.terminal.console_print("\r" + self.console_str)
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.interpretador_comando(self.console_str)
			self.console_str = ""
		
	def handle_interrupt (self, interrupt):
		if interrupt == pycfg.INTERRUPT_KEYBOARD:
			self.interrupt_keyboard()
	
	
	def interpretador_comando (self, comando):
		if comando == "sair":
			self.cpu.cpu_alive = False
		elif comando == "abrir":
			self.terminal.console_print("Carregando processo" + "\n")
		else:
			self.terminal.console_print("Comando invalido " + comando + "\n")

	
	def syscall (self):
		self.estrutura_processo.estado = str("Processo em execucao")
		self.terminal.console_print("Executando chamada de sistema" + "\n")
		return
		
	def interrupcao (self):
		self.estrutura_processo.estado = str("Processo bloqueado")
		self.terminal.console_print("Sistema interrompido" + "\n")
		return
