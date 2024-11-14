export enum TemplateStatus {
    ACTIVO = 'ACTIVO',
    INACTIVO = 'INACTIVO'
}

export interface Template {
    diseno_pdf_id: number;
    nombre: string;
    link_archivo: string;
    estado: TemplateStatus;
    created_at: string;
    updated_at: string;
}