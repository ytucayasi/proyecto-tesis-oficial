import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalGenerateComponent } from './modal-generate.component';

describe('ModalGenerateComponent', () => {
  let component: ModalGenerateComponent;
  let fixture: ComponentFixture<ModalGenerateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModalGenerateComponent]
    });
    fixture = TestBed.createComponent(ModalGenerateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
