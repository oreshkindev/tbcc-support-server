from datetime import datetime

from service.db.database import database
from service.model.report import report_table
from service.schema import report as report_schema
from sqlalchemy import desc, func, select


async def create_report(report: report_schema.ReportModel):
    query = (
        report_table.insert()
        .values(
            title=report.title,
            category=report.category,
            content=report.content,
            status=report.status,
            created_at=datetime.now(),
        )
        .returning(
            report_table.c.id,
            report_table.c.title,
            report_table.c.category,
            report_table.c.content,
            report_table.c.status,
            report_table.c.created_at,
        )
    )
    report = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    report = dict(zip(report, report.values()))
    return report


async def get_report(report_id: int):
    query = (
        select(
            [
                report_table.c.id,
                report_table.c.title,
                report_table.c.category,
                report_table.c.content,
                report_table.c.status,
                report_table.c.created_at,
            ]
        )
        .select_from(report_table)
        .where(report_table.c.id == report_id)
    )
    return await database.fetch_one(query)


async def get_reports(page: int):
    max_per_page = 100
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                report_table.c.id,
                report_table.c.title,
                report_table.c.category,
                report_table.c.content,
                report_table.c.status,
                report_table.c.created_at,
            ]
        )
        .select_from(report_table)
        .order_by(desc(report_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_reports_count():
    query = select([func.count()]).select_from(report_table)
    return await database.fetch_val(query)


async def update_report(report_id: int, report: report_schema.ReportModel):
    query = (
        report_table.update()
        .where(report_table.c.id == report_id)
        .values(
            title=report.title,
            category=report.category,
            content=report.content,
            status=report.status,
        )
    )
    return await database.execute(query)


async def delete_reports(report_id: str):
    query = report_table.delete().where(report_id == report_table.c.report_id)
    return await database.execute(query)