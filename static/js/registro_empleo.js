/**
 * Script para la gestión de Registro de Empleos
 */

document.addEventListener('DOMContentLoaded', () => {
    const empleoForm = document.getElementById('empleoForm');
    const empleosList = document.getElementById('empleosList');
    const empleosCount = document.getElementById('empleosCount');
    const emptyState = document.getElementById('emptyState');

    let empleos = [];

    // Cargar empleos al iniciar
    loadEmpleos();

    // Manejar el envío del formulario
    empleoForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const nombreEmpresa = document.getElementById('nombreEmpresa').value.trim();
        const linkEmpleo = document.getElementById('linkEmpleo').value.trim();

        if (!nombreEmpresa) {
            alert('Por favor ingresa el nombre de la empresa');
            return;
        }

        // Crear nuevo empleo
        const nuevoEmpleo = {
            id: Date.now(),
            nombreEmpresa,
            linkEmpleo: linkEmpleo || '', // Permitir link vacío
            fecha: new Date().toISOString()
        };

        // Agregar a la lista
        empleos.push(nuevoEmpleo);

        // Guardar en el servidor
        await saveEmpleos();

        // Limpiar formulario
        empleoForm.reset();

        // Actualizar vista
        renderEmpleos();
    });

    /**
     * Abrir modal con detalles del empleo
     */
    function openEmpleoModal(id) {
        const empleo = empleos.find(e => e.id === id);
        if (!empleo) return;

        const modal = document.getElementById('empleoModal');
        const modalEmpresa = document.getElementById('modalEmpresa');
        const modalLink = document.getElementById('modalLink');
        const modalFecha = document.getElementById('modalFecha');

        // Llenar datos del modal
        modalEmpresa.textContent = empleo.nombreEmpresa;

        if (empleo.linkEmpleo) {
            modalLink.innerHTML = `<a href="${escapeHtml(empleo.linkEmpleo)}" target="_blank" rel="noopener noreferrer">${escapeHtml(empleo.linkEmpleo)}</a>`;
        } else {
            modalLink.innerHTML = '<span style="color: #a0aec0; font-style: italic;">No se proporcionó un link</span>';
        }

        const fecha = new Date(empleo.fecha);
        const fechaFormateada = fecha.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        modalFecha.textContent = fechaFormateada;

        // Mostrar modal
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Cerrar modal
     */
    function closeEmpleoModal() {
        const modal = document.getElementById('empleoModal');
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    /**
     * Cargar empleos desde el servidor
     */
    async function loadEmpleos() {
        try {
            const response = await fetch('/get_empleos');
            const data = await response.json();
            empleos = data.empleos || [];
            renderEmpleos();
        } catch (error) {
            console.error('Error al cargar empleos:', error);
            empleos = [];
            renderEmpleos();
        }
    }

    /**
     * Guardar empleos en el servidor
     */
    async function saveEmpleos() {
        try {
            const response = await fetch('/save_empleos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ empleos })
            });

            const result = await response.json();
            if (!result.success) {
                throw new Error('Error al guardar');
            }
        } catch (error) {
            console.error('Error al guardar empleos:', error);
            alert('Error al guardar los empleos. Por favor intenta de nuevo.');
        }
    }

    /**
     * Eliminar un empleo
     */
    async function deleteEmpleo(id) {
        if (!confirm('¿Estás seguro de que deseas eliminar este empleo?')) {
            return;
        }

        empleos = empleos.filter(empleo => empleo.id !== id);
        await saveEmpleos();
        renderEmpleos();
    }

    /**
     * Renderizar la lista de empleos
     */
    function renderEmpleos() {
        // Actualizar contador
        const count = empleos.length;
        empleosCount.textContent = `${count} empleo${count !== 1 ? 's' : ''}`;

        // Mostrar/ocultar estado vacío
        if (count === 0) {
            emptyState.style.display = 'block';
            empleosList.innerHTML = '';
            empleosList.appendChild(emptyState);
            return;
        }

        emptyState.style.display = 'none';

        // Renderizar empleos (más recientes primero)
        const empleosOrdenados = [...empleos].reverse();
        empleosList.innerHTML = empleosOrdenados.map(empleo => {
            const fecha = new Date(empleo.fecha);
            const fechaFormateada = fecha.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });

            // Generar HTML del link si existe
            const linkHtml = empleo.linkEmpleo
                ? `<a href="${escapeHtml(empleo.linkEmpleo)}" target="_blank" rel="noopener noreferrer">
                    <svg xmlns="http://www.w3.org/2000/svg" style="width: 14px; height: 14px; display: inline-block; vertical-align: middle; margin-right: 4px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                    ${escapeHtml(empleo.linkEmpleo)}
                </a>`
                : `<div style="color: #a0aec0; font-size: 0.9rem; font-style: italic; margin-bottom: 0.75rem;">
                    <svg xmlns="http://www.w3.org/2000/svg" style="width: 14px; height: 14px; display: inline-block; vertical-align: middle; margin-right: 4px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                    Sin link
                </div>`;

            return `
                <div class="empleo-item">
                    <h3>${escapeHtml(empleo.nombreEmpresa)}</h3>
                    <div class="empleo-fecha">
                        <svg xmlns="http://www.w3.org/2000/svg" style="width: 14px; height: 14px; display: inline-block; vertical-align: middle; margin-right: 4px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Agregado: ${fechaFormateada}
                    </div>
                    ${linkHtml}
                    <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                        <button class="btn-view" onclick="window.openEmpleoModalById(${empleo.id})">
                            <svg xmlns="http://www.w3.org/2000/svg" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle; margin-right: 4px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                            Ver
                        </button>
                        <button class="btn-delete" onclick="window.deleteEmpleoById(${empleo.id})">
                            <svg xmlns="http://www.w3.org/2000/svg" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle; margin-right: 4px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                            Eliminar
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    /**
     * Escapar HTML para prevenir XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Exponer funciones globalmente
    window.deleteEmpleoById = deleteEmpleo;
    window.openEmpleoModalById = openEmpleoModal;
    window.closeEmpleoModal = closeEmpleoModal;
});
