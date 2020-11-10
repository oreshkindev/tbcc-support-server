from service.schema.report import ReportDetailsModel, ReportModel
from service.schema.user import User
from service.util import report as report_util
from service.util.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post(
    "", response_model=ReportDetailsModel, status_code=201, name="create report"
)
async def create_report(
    report: ReportModel, current_user: User = Depends(get_current_user)
):
    report = await report_util.create_report(report)
    return report


@router.get("")
async def get_reports(page: int = 1, current_user: User = Depends(get_current_user)):
    total_cout = await report_util.get_reports_count()
    report = await report_util.get_reports(page)
    return {"total_count": total_cout, "results": report}


@router.get("/{report_id}", response_model=ReportDetailsModel, name="get report by id")
async def get_report(report_id: int, current_user: User = Depends(get_current_user)):
    return await report_util.get_report(report_id)


@router.put(
    "/{report_id}", response_model=ReportDetailsModel, name="update report by id"
)
async def update_report(
    report_id: int,
    report_data: ReportModel,
    current_user: User = Depends(get_current_user),
):
    report = await report_util.get_report(report_id)

    await report_util.update_report(report_id=report_id, report=report_data)
    return await report_util.get_report(report_id)


@router.delete("/{from_id}", name="remove report by id")
async def delete_reports(from_id: str, current_user: User = Depends(get_current_user)):

    await report_util.delete_reports(from_id)