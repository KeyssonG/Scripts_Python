import subprocess
import os
import datetime
import logging
import time
import schedule
import getpass
from pathlib import Path

class PostgreSQLBackup:
    def __init__(self, host='localhost', port='5432', database=None, username=None, password=None):
        """
        Inicializa a classe de backup do PostgreSQL
        
        Args:
            host (str): Host do banco de dados
            port (str): Porta do banco de dados
            database (str): Nome do banco de dados
            username (str): Nome de usuário
            password (str): Senha do usuário
        """
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.backup_dir = Path("/home/keysson/Documentos/backupPostgres")
        # Configura logging
        self._setup_logging()
        # Cria diretório de backup se não existir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        log_file = self.backup_dir / 'backup.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _generate_filename(self):
        """Gera nome do arquivo de backup com timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.database}_backup_{timestamp}.sql"
    
    def create_backup(self):
        """
        Cria backup do banco PostgreSQL usando pg_dump
        
        Returns:
            bool: True se backup foi criado com sucesso, False caso contrário
        """
        try:
            # Gera nome do arquivo
            filename = self._generate_filename()
            backup_path = self.backup_dir / filename
            
            # Caminho do pg_dump no Linux (assume que está no PATH)
            pg_dump_path = "pg_dump"
            
            # Comando pg_dump
            cmd = [
                pg_dump_path,
                f'--host={self.host}',
                f'--port={self.port}',
                f'--username={self.username}',
                '--no-password',
                '--verbose',
                '--clean',
                '--no-owner',
                '--no-privileges',
                f'--file={backup_path}',
                self.database
            ]
            
            # Configura variável de ambiente para senha
            env = os.environ.copy()
            if self.password:
                env['PGPASSWORD'] = self.password
            
            self.logger.info(f"Iniciando backup do banco '{self.database}'...")
            
            # Executa comando
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            self.logger.info(f"Backup criado com sucesso: {backup_path}")
            self.logger.info(f"Tamanho do arquivo: {backup_path.stat().st_size / (1024*1024):.2f} MB")
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao executar pg_dump: {e}")
            self.logger.error(f"Stderr: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Erro inesperado: {e}")
            return False
    
    def cleanup_old_backups(self, days_to_keep=7):
        """
        Remove backups antigos
        
        Args:
            days_to_keep (int): Número de dias para manter os backups
        """
        try:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_to_keep)
            
            for backup_file in self.backup_dir.glob("*.sql"):
                file_time = datetime.datetime.fromtimestamp(backup_file.stat().st_mtime)
                
                if file_time < cutoff_date:
                    backup_file.unlink()
                    self.logger.info(f"Backup antigo removido: {backup_file.name}")
                    
        except Exception as e:
            self.logger.error(f"Erro ao limpar backups antigos: {e}")

def get_database_config():
    """Coleta informações do banco de dados do usuário"""
    print("=" * 60)
    print("CONFIGURAÇÃO DO BANCO POSTGRESQL")
    print("=" * 60)
    print("Por segurança, todos os dados serão ocultados durante a digitação")
    print("=" * 60)
    
    # Host do banco
    host_input = getpass.getpass("Host do banco (pressione Enter para localhost): ").strip()
    host = host_input if host_input else 'localhost'
    
    # Porta do banco
    port_input = getpass.getpass("Porta do banco (pressione Enter para 5432): ").strip()
    port = port_input if port_input else '5432'
    
    # Nome do banco de dados (obrigatório)
    database = getpass.getpass("Nome do banco de dados: ").strip()
    
    # Nome de usuário (obrigatório)
    username = getpass.getpass("Nome de usuário: ").strip()
    
    # Senha
    password = getpass.getpass("Senha: ")
    
    if not database or not username:
        print("Nome do banco e usuário são obrigatórios!")
        return None
    
    confirm = input("\nConfirmar configuração? (s/N): ").strip().lower()
    if confirm not in ['s', 'sim', 'y', 'yes']:
        print("Configuração cancelada!")
        return None
    
    return {
        'host': host,
        'port': port,
        'database': database,
        'username': username,
        'password': password
    }

def show_menu():
    """Mostra o menu de opções"""
    print("\n" + "=" * 60)
    print("OPÇÕES DE BACKUP")
    print("=" * 60)
    print("1.Executar backup agora (único)")
    print("2.Configurar backup automático")
    print("3.Sair")
    print("=" * 60)
    
    while True:
        try:
            choice = int(input("Escolha uma opção (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Opção inválida! Digite 1, 2 ou 3.")
        except ValueError:
            print("Digite apenas números!")

def show_schedule_menu():
    """Mostra o menu de agendamento"""
    print("\n" + "=" * 60)
    print("OPÇÕES DE AGENDAMENTO")
    print("=" * 60)
    print("1.Backup diário às 02:00")
    print("2.Backup a cada 6 horas")
    print("3.Backup semanal (segunda-feira às 02:00)")
    print("4.Backup a cada 2 dias às 02:00")
    print("5.Backup a cada 30 minutos (teste)")
    print("6.Personalizar horário")
    print("7. <- Voltar ao menu principal")
    print("=" * 60)
    
    while True:
        try:
            choice = int(input("Escolha uma opção (1-7): "))
            if choice in range(1, 8):
                return choice
            else:
                print("Opção inválida! Digite um número de 1 a 7.")
        except ValueError:
            print("Digite apenas números!")

def get_custom_schedule():
    """Permite ao usuário configurar um horário personalizado"""
    print("\nCONFIGURAÇÃO PERSONALIZADA")
    print("=" * 40)
    print("Opções disponíveis:")
    print("1. Diário em horário específico")
    print("2. A cada X horas")
    print("3. Dia da semana específico")
    
    try:
        option = int(input("Escolha o tipo (1-3): "))
        
        if option == 1:
            time_str = input("Digite o horário (formato HH:MM, ex: 14:30): ")
            try:
                # Valida formato
                datetime.datetime.strptime(time_str, "%H:%M")
                return ("daily", time_str)
            except ValueError:
                print("Formato inválido! Use HH:MM")
                return None
                
        elif option == 2:
            hours = int(input("A cada quantas horas? "))
            if hours > 0:
                return ("hours", hours)
            else:
                print("Número de horas deve ser maior que 0!")
                return None
                
        elif option == 3:
            print("Dias da semana:")
            print("1-Segunda, 2-Terça, 3-Quarta, 4-Quinta, 5-Sexta, 6-Sábado, 7-Domingo")
            day = int(input("Escolha o dia (1-7): "))
            time_str = input("Digite o horário (HH:MM): ")
            
            if 1 <= day <= 7:
                try:
                    datetime.datetime.strptime(time_str, "%H:%M")
                    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                    return ("weekly", days[day-1], time_str)
                except ValueError:
                    print("Formato de horário inválido!")
                    return None
            else:
                print("Dia inválido!")
                return None
        else:
            print("Opção inválida!")
            return None
            
    except ValueError:
        print("Digite apenas números!")
        return None

def main():
    """Função principal interativa para executar o backup"""
    
    print("SISTEMA DE BACKUP POSTGRESQL")
    print("=" * 60)
    
    # Coleta configurações do banco
    backup_config = get_database_config()
    if not backup_config:
        return
    
    # Mostra menu de opções
    while True:
        choice = show_menu()
        
        if choice == 1:
            # Backup único
            print("\nIniciando backup único...")
            try:
                backup = PostgreSQLBackup(**backup_config)
                success = backup.create_backup()
                
                if success:
                    backup.cleanup_old_backups(days_to_keep=7)
                    print("Backup realizado com sucesso!")
                else:
                    print("Falha ao realizar backup!")
                    
            except Exception as e:
                print(f"Erro na execução: {e}")
            
            input("\nPressione Enter para continuar...")
            
        elif choice == 2:
            # Backup automático
            schedule_choice = show_schedule_menu()
            
            if schedule_choice == 7:
                continue  # Volta ao menu principal
            
            # Configura o agendamento
            schedule_config = None
            
            if schedule_choice == 1:
                schedule_config = ("daily", "02:00")
            elif schedule_choice == 2:
                schedule_config = ("hours", 6)
            elif schedule_choice == 3:
                schedule_config = ("weekly", "monday", "02:00")
            elif schedule_choice == 4:
                schedule_config = ("days", 2, "02:00")
            elif schedule_choice == 5:
                schedule_config = ("minutes", 30)
            elif schedule_choice == 6:
                schedule_config = get_custom_schedule()
            
            if schedule_config:
                run_scheduled_backup(backup_config, schedule_config)
            
        elif choice == 3:
            print("Saindo... Até mais!")
            break

def run_scheduled_backup(backup_config, schedule_config):
    """Executa backup com agendamento automático"""
    
    def backup_job():
        """Job de backup para o agendador"""
        try:
            backup = PostgreSQLBackup(**backup_config)
            success = backup.create_backup()
            
            if success:
                backup.cleanup_old_backups(days_to_keep=7)
                print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Backup automático realizado com sucesso!")
            else:
                print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Falha no backup automático!")
                
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Erro no backup automático: {e}")
    
    # Limpa agendamentos anteriores
    schedule.clear()
    
    # Configura o agendamento baseado na escolha do usuário
    schedule_type = schedule_config[0]
    
    if schedule_type == "daily":
        time_str = schedule_config[1]
        schedule.every().day.at(time_str).do(backup_job)
        print(f"Backup agendado: Diário às {time_str}")
        
    elif schedule_type == "hours":
        hours = schedule_config[1]
        schedule.every(hours).hours.do(backup_job)
        print(f"Backup agendado: A cada {hours} horas")
        
    elif schedule_type == "weekly":
        day = schedule_config[1]
        time_str = schedule_config[2]
        getattr(schedule.every(), day).at(time_str).do(backup_job)
        print(f"Backup agendado: Toda {day} às {time_str}")
        
    elif schedule_type == "days":
        days = schedule_config[1]
        time_str = schedule_config[2]
        schedule.every(days).days.at(time_str).do(backup_job)
        print(f"Backup agendado: A cada {days} dias às {time_str}")
        
    elif schedule_type == "minutes":
        minutes = schedule_config[1]
        schedule.every(minutes).minutes.do(backup_job)
        print(f"Backup agendado: A cada {minutes} minutos")
    
    print("\nAgendador de backup iniciado...")
    
    # Mostra próximo backup agendado se houver
    try:
        next_run = schedule.next_run()
        if next_run:
            print(f"Próximo backup: {next_run.strftime('%d/%m/%Y %H:%M:%S')}")
    except:
        print("Próximo backup: Em breve...")
    
    print("Pressione Ctrl+C para parar e voltar ao menu\n")
    
    # Executa um backup imediatamente ao iniciar
    print("Executando backup inicial...")
    backup_job()
    
    # Loop principal do agendador
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto
    except KeyboardInterrupt:
        print("\nAgendador interrompido pelo usuário")
        print("Voltando ao menu principal...\n")
        schedule.clear()  # Limpa agendamentos

if __name__ == "__main__":
    main()
    