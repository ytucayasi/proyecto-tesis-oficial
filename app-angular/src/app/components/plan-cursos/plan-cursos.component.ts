import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faPlay } from '@fortawesome/free-solid-svg-icons';
import { ModalGenerateComponent } from '../modal-generate/modal-generate.component';
import { LoadingComponent } from '../loading/loading.component';
import { Template } from 'src/app/interfaces/template';
import { TemplateService } from 'src/app/services/template.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ResourceService } from 'src/app/services/resource.service';
import { ResourceRequest } from 'src/app/interfaces/resource-request';
import { ResourceResponse } from 'src/app/interfaces/resource-response';

@Component({
  selector: 'app-plan-cursos',
  templateUrl: './plan-cursos.component.html',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    FontAwesomeModule,
    ModalGenerateComponent,
    LoadingComponent,
    HttpClientModule
  ],
  providers: [TemplateService, ResourceService],
  styleUrls: ['./plan-cursos.component.css']
})
export class PlanCursosComponent {

  constructor(private resourceService: ResourceService) { }

  courseInfo = {
    title: 'Introducción a auditoria en los sistema',
    university: 'Universidad Peruana Unión',
    department: 'Vicerrectorado académico',
    office: 'Oficina de gestión curricular y gabinete pedagógico',
    structure: 'Estructura del plan de clase en el lamb',
    semester: 'Semestre 2024-2',
    unit: 'APRENDIZAJE SUPERVISADO, NO SUPERVISADO Y POR REFUERZO',
    session: 'N° 6',
    date: '13/10/2024',
    topic: 'Introducción a auditoria en los sistema'
  };
  modelos = [
    {
      id: 1,
      nombre: 'Llama 90 B',
      modelo: "llama-90b"
    },
    {
      id: 2,
      nombre: 'Llama 9 B',
      modelo: "gemma-9b"
    },
    {
      id: 3,
      nombre: 'Llama 3 B',
      modelo: "llama-3b"
    },
    {
      id: 4,
      nombre: 'Llama 70 B',
      modelo: "llama-70b"
    }
  ]
  selectedModelo = this.modelos[0];
  plantillas = [
    {
      id: 1,
      nombre: 'Plantilla Word',
      plantilla: 1,
      tipo: "word"
    },
    {
      id: 2,
      nombre: 'Plantilla PPT',
      plantilla: 9,
      tipo: "ppt"
    },
    {
      id: 3,
      nombre: 'Plantilla PDF',
      plantilla: 9,
      tipo: "pdf"
    },
  ]
  selectedPlantilla = this.plantillas[0];
  sections = [
    {
      id: 1,
      title: 'INICIO - Motivación',
      resources: [
        { type: 'PPT', pages: 5, template: 4, status: 'none' as const },
        { type: 'PDF', pages: 5, template: 4, status: 'none' as const }
      ]
    },
    {
      id: 2,
      title: 'EXPLICA - Guía Teórica',
      resources: [
        { type: 'PPT', pages: 5, template: 4, status: 'none' as const },
        { type: 'PDF', pages: 5, template: 4, status: 'none' as const }
      ]
    },
    {
      id: 3,
      title: 'APLICA - Guía Práctica',
      resources: [
        { type: 'PPT', pages: 5, template: 1, status: 'none' as const },
        { type: 'PDF', pages: 5, template: 1, status: 'none' as const },
        { type: 'Rubrica', pages: 5, template: 1, status: 'none' as const }
      ]
    },
    {
      id: 4,
      title: 'CREA - Actividad Autónoma',
      resources: [
        { type: 'PPT', pages: 5, template: 1, status: 'none' as const },
        { type: 'PDF', pages: 5, template: 1, status: 'none' as const },
        { type: 'Rubrica', pages: 5, template: 1, status: 'none' as const }
      ]
    }
  ];

  /* Secciones */
  activeSection = 'Recursos';

  file: File | null = null;
  resourceResponse: ResourceResponse | null = null;

  onFileSelected(event: any) {
    const files = event.target.files;
    if (files.length > 0) {
      this.file = files[0];
    }
  }

  setActiveSection(section: string) {
    this.activeSection = section;
  }
  /* Modal */
  faPlay = faPlay;
  isLoading = false;
  isModalOpen = false;

  startGeneration() {
    this.isModalOpen = false;
    this.isLoading = true;

    if (!this.file) {
      console.error('No file selected');
      return;
    }

    const data: ResourceRequest = {
      file: this.file,
      titulo: this.courseInfo.title,
      modelo: this.selectedModelo.modelo,
      diseno: this.selectedPlantilla.plantilla,
      tipo_recurso: this.selectedPlantilla.tipo,
      cantidad_paginas: '10'
    };

    this.resourceService.generateResource(data).subscribe({
      next: (response) => {
        this.resourceResponse = response;
        this.isLoading = false;
        this.openModal();
        console.log('Resource generated:', response);
      },
      error: (error) => {
        this.isLoading = false;
        console.error('Error generating resource:', error);
        // Handle error appropriately
      }
    });
  }

  openModal() {
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
  }

  onGenerate() {
    console.log('Generando recursos...');
    this.closeModal();
  }

  /* Mostrar contenido */
  selectedResources: { [key: string]: boolean } = {};

  // Método para manejar los cambios en los checkboxes
  toggleResource(sectionId: number, resourceType: string): void {
    const key = `${sectionId}-${resourceType}`;
    this.selectedResources[key] = !this.selectedResources[key];
  }

  // Método para verificar si un recurso está seleccionado
  isResourceSelected(sectionId: number, resourceType: string): boolean {
    return this.selectedResources[`${sectionId}-${resourceType}`] || false;
  }
}