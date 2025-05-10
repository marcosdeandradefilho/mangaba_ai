import logging
import sys
from pathlib import Path
from typing import Optional

class Logger:
    """Classe para gerenciamento centralizado de logs."""
    
    _instance: Optional['Logger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """Configura o logger com handlers para console e arquivo."""
        self.logger = logging.getLogger('mangaba_ai')
        self.logger.setLevel(logging.DEBUG)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para arquivo
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_dir / 'mangaba_ai.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Registra mensagem de debug."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Registra mensagem informativa."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Registra mensagem de aviso."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Registra mensagem de erro."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Registra mensagem crítica."""
        self.logger.critical(message)

# Instância global do logger
logger = Logger() 