from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs import marcar_tarefas_nao_realizadas

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")


def iniciar_scheduler():
    scheduler.add_job(
        marcar_tarefas_nao_realizadas,
        trigger="cron",
        hour=0,
        minute=5,
        id="marcar_nao_realizadas",
        replace_existing=True,
    )
    scheduler.start()