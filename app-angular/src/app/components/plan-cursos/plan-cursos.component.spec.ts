import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlanCursosComponent } from './plan-cursos.component';

describe('PlanCursosComponent', () => {
  let component: PlanCursosComponent;
  let fixture: ComponentFixture<PlanCursosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PlanCursosComponent]
    });
    fixture = TestBed.createComponent(PlanCursosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
