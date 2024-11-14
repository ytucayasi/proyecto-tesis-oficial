import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Template } from '../interfaces/template';

@Injectable({
  providedIn: 'root'
})
export class TemplateService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getTemplates(): Observable<Template[]> {
    return this.http.get<Template[]>(`${this.apiUrl}/diseno-pdf`);
  }
}