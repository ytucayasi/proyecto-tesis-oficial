// loading.component.ts
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="show" class="fixed inset-0 z-50 overflow-y-auto">
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-50"></div>
      
      <!-- Loading Content -->
      <div class="flex min-h-full items-center justify-center p-4">
        <div class="relative bg-white rounded-lg shadow-xl w-full max-w-md p-6">
          <div class="text-center">
            <div class="mb-4">
              <!-- Circular Progress Animation -->
              <div class="w-24 h-24 border-4 border-blue-200 border-t-[#001C48] rounded-full animate-spin mx-auto"></div>
            </div>
            
            <h3 class="text-lg font-semibold text-gray-900 mb-4">GENERANDO RECURSO...</h3>
            
            <!-- Progress Bar -->
            <div class="w-full bg-gray-200 rounded-full h-2.5 mb-2">
              <div class="bg-[#001C48] h-2.5 rounded-full transition-all duration-300"
                   [style.width]="progress + '%'">
              </div>
            </div>
            
            <!-- Progress Percentage -->
            <p class="text-sm text-gray-600">{{ progress }}%</p>
          </div>
        </div>
      </div>
    </div>
  `
})
export class LoadingComponent implements OnChanges {
  @Input() show = false;
  progress = 0;
  private interval: any;

  ngOnChanges(changes: SimpleChanges) {
    if (changes['show']) {
      if (changes['show'].currentValue) {
        // Si el componente se muestra, iniciamos el progreso
        this.resetAndStartProgress();
      } else {
        // Si el componente se oculta, limpiamos el intervalo
        this.cleanupInterval();
      }
    }
  }

  ngOnDestroy() {
    this.cleanupInterval();
  }

  private resetAndStartProgress() {
    // Limpiamos cualquier intervalo existente
    this.cleanupInterval();

    // Reiniciamos el progreso
    this.progress = 0;

    // Iniciamos nuevo progreso
    const duration = 10000; // 10 segundos
    const steps = 100;
    const increment = 100 / steps;
    const stepDuration = duration / steps;

    this.interval = setInterval(() => {
      if (this.progress < 100) {
        this.progress += increment;
      } else {
        this.cleanupInterval();
      }
    }, stepDuration);
  }

  private cleanupInterval() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  }
}