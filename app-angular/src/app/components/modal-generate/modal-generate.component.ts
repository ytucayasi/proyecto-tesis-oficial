import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faTimes, faDownload, faEye } from '@fortawesome/free-solid-svg-icons';
import { ResourceResponse } from 'src/app/interfaces/resource-response';
import { ResourceService } from 'src/app/services/resource.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

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
  @Input() resourceResponse: ResourceResponse | null = null;
  
  faTimes = faTimes;
  faDownload = faDownload;
  faEye = faEye;
  documentUrl: SafeResourceUrl | null = null;
  isViewing = false;

  constructor(
    private resourceService: ResourceService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnChanges() {
    if (this.resourceResponse?.resource_path) {
      const filename = this.resourceResponse.resource_path.split('/').pop();
      this.documentUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
        this.resourceService.getViewUrl(filename!)
      );
    }
  }

  downloadDocument() {
    if (this.resourceResponse?.resource_path) {
      const filename = this.resourceResponse.resource_path.split('/').pop();
      window.open(this.resourceService.getFileUrl(filename!));
    }
  }

  viewDocument() {
    this.isViewing = !this.isViewing;
  }

  closeModal() {
    this.close.emit();
  }

  onGenerate() {
    this.generate.emit();
  }
}