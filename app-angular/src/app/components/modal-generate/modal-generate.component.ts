// modal-generate.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-modal-generate',
  standalone: true,
  imports: [CommonModule, FontAwesomeModule],
  templateUrl: './modal-generate.component.html',
  styleUrls: ['./modal-generate.component.css']
})
export class ModalGenerateComponent {
  @Input() isOpen = false;
  @Output() close = new EventEmitter<void>();
  @Output() generate = new EventEmitter<void>();
  
  faTimes = faTimes;

  closeModal() {
    this.close.emit();
  }

  onGenerate() {
    this.generate.emit();
  }
}