"""Entry point do pipeline ETL"""
import argparse
import sys
from src.etl.config import SDW_API_URL, LOG_LEVEL
from src.etl.utils import setup_logging
from src.etl.extract import read_csv, extract_users
from src.etl.transform import transform_users
from src.etl.load import load_users

def parse_args():
    """Parse argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="Pipeline ETL - Santander Dev Week 2023"
    )
    parser.add_argument(
        "--csv",
        type=str,
        required=True,
        help="Caminho do arquivo CSV com UserIDs"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["real", "mock"],
        default="mock",
        help="Modo de execução: 'real' (OpenAI + API) ou 'mock' (local)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa sem fazer atualizações reais na API"
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default=SDW_API_URL,
        help="URL base da API (padrão: SDW_API_URL do .env)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=LOG_LEVEL,
        help="Nível de log"
    )
    
    return parser.parse_args()

def main():
    """Função principal do pipeline ETL"""
    args = parse_args()
    logger = setup_logging(args.log_level)
    
    logger.info("=" * 60)
    logger.info("Iniciando Pipeline ETL - Santander Dev Week 2023")
    logger.info(f"Modo: {args.mode.upper()}")
    logger.info(f"CSV: {args.csv}")
    logger.info(f"API URL: {args.api_url}")
    logger.info(f"Dry Run: {args.dry_run}")
    logger.info("=" * 60)
    
    try:
        # EXTRACT
        logger.info("\n[EXTRACT] Iniciando extração de dados...")
        user_ids = read_csv(args.csv)
        
        if not user_ids:
            logger.error("Nenhum ID encontrado no CSV")
            sys.exit(1)
        
        users = extract_users(user_ids, args.api_url)
        
        if not users:
            logger.error("Nenhum usuário válido encontrado")
            sys.exit(1)
        
        # TRANSFORM
        logger.info("\n[TRANSFORM] Iniciando transformação e geração de mensagens...")
        users = transform_users(users, args.mode)
        
        # LOAD
        logger.info("\n[LOAD] Iniciando carregamento e atualização...")
        stats = load_users(users, args.api_url, args.dry_run)
        
        # SUMMARY
        logger.info("\n" + "=" * 60)
        logger.info("Pipeline ETL concluído!")
        logger.info(f"Total de usuários processados: {len(users)}")
        logger.info(f"Atualizações bem-sucedidas: {stats['success']}")
        logger.info(f"Atualizações falhadas: {stats['failed']}")
        logger.info(f"Atualizações puladas: {stats['skipped']}")
        logger.info("=" * 60)
        
        if stats['failed'] > 0:
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.warning("\nPipeline interrompido pelo usuário")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\nErro fatal no pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
