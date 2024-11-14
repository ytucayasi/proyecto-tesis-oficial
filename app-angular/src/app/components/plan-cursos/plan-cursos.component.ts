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

interface Resource {
  id: number;
  title: string;
  type: 'PPT' | 'PDF' | 'Rubrica';
  pages: number;
  template: number;
  status: 'complete' | 'partial' | 'none';
}

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
  providers: [TemplateService],
  styleUrls: ['./plan-cursos.component.css']
})
export class PlanCursosComponent {


  templates: Template[] = [];
  selectedTemplate: number | null = null;

  constructor(private templateService: TemplateService) { }

  ngOnInit() {
    this.loadTemplates();
  }

  loadTemplates() {
    this.templateService.getTemplates().subscribe({
      next: (templates) => {
        this.templates = templates;
      },
      error: (error) => {
        console.error('Error loading templates:', error);
      }
    });
  }

  selectTemplate(templateId: number) {
    this.selectedTemplate = templateId;
  }


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

  setActiveSection(section: string) {
    this.activeSection = section;
  }
  /* Modal */
  faPlay = faPlay;
  isLoading = false;
  isModalOpen = false;

  startGeneration() {
    // Asegurarnos de que todo esté cerrado antes de empezar
    this.isModalOpen = false;
    this.isLoading = true;

    setTimeout(() => {
      this.isLoading = false;
      this.openModal();
    }, 10000);
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