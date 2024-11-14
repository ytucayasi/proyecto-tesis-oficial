import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CursosCargaComponent } from './cursos-carga.component';

describe('CursosCargaComponent', () => {
  let component: CursosCargaComponent;
  let fixture: ComponentFixture<CursosCargaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CursosCargaComponent]
    });
    fixture = TestBed.createComponent(CursosCargaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
