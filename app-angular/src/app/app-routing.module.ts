import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PlanCursosComponent } from './components/plan-cursos/plan-cursos.component';
import { CursosCargaComponent } from './components/cursos-carga/cursos-carga.component';

const routes: Routes = [
  { path: 'plan-cursos', component: PlanCursosComponent },
  { path: 'cursos-carga', component: CursosCargaComponent },
  { path: '', redirectTo: '/plan-cursos', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
