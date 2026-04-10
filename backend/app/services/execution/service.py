from sqlalchemy.orm import Session

from app.domain.models import AuditLog, ExecutionPlan, RollbackSnapshot


class ExecutionService:
    def create_plan(self, db: Session, plan_name: str, steps: list[dict], dry_run: bool) -> ExecutionPlan:
        plan = ExecutionPlan(plan_name=plan_name, steps_json=steps, dry_run=dry_run, status='pending')
        db.add(plan)
        db.flush()

        snapshot = RollbackSnapshot(plan_id=plan.id, snapshot_json={'steps': steps, 'pre_state': 'captured'})
        db.add(snapshot)
        db.add(AuditLog(actor='system', action='plan.created', target=f'plan:{plan.id}', details={'dry_run': dry_run}))
        db.commit()
        db.refresh(plan)
        return plan

    def execute_plan(self, db: Session, plan: ExecutionPlan, approved: bool) -> ExecutionPlan:
        if not approved:
            plan.status = 'blocked'
        elif plan.dry_run:
            plan.status = 'simulated'
        else:
            plan.status = 'applied'
        db.add(AuditLog(actor='system', action='plan.executed', target=f'plan:{plan.id}', details={'status': plan.status}))
        db.commit()
        db.refresh(plan)
        return plan
