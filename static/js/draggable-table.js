/**
 * SmartLogX - Draggable Table Columns
 * Zoho Projects Style with Persistent Column Order
 */

class DraggableTable {
    constructor(tableId, tableName, saveUrl) {
        this.table = document.getElementById(tableId);
        this.tableName = tableName;
        this.saveUrl = saveUrl;
        this.draggedColumn = null;
        this.draggedIndex = null;
        this.placeholder = null;
        this.storageKey = `table_${tableName}_colOrder`;
        
        if (this.table) {
            this.init();
        }
    }
    
    init() {
        this.headerRow = this.table.querySelector('thead tr');
        this.headers = Array.from(this.headerRow.querySelectorAll('th[data-column]'));
        
        // Load saved order
        this.loadColumnOrder();
        
        // Setup drag events
        this.setupDragEvents();
    }
    
    loadColumnOrder() {
        // Try localStorage first
        let savedOrder = localStorage.getItem(this.storageKey);
        
        if (savedOrder) {
            try {
                savedOrder = JSON.parse(savedOrder);
                this.reorderColumns(savedOrder);
            } catch (e) {
                console.error('Error loading column order:', e);
            }
        }
    }
    
    saveColumnOrder() {
        const order = this.headers.map(th => th.dataset.column);
        
        // Save to localStorage
        localStorage.setItem(this.storageKey, JSON.stringify(order));
        
        // Save to server (optional)
        if (this.saveUrl && typeof csrfToken !== 'undefined') {
            fetch(this.saveUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    table_name: this.tableName,
                    column_order: order
                })
            }).catch(err => console.log('Column order save error:', err));
        }
    }
    
    reorderColumns(order) {
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        // Create column index map
        const currentOrder = this.headers.map(th => th.dataset.column);
        const newIndexMap = {};
        
        order.forEach((col, newIndex) => {
            const oldIndex = currentOrder.indexOf(col);
            if (oldIndex !== -1) {
                newIndexMap[oldIndex] = newIndex;
            }
        });
        
        // Reorder header
        const sortedHeaders = [...this.headers].sort((a, b) => {
            const aIndex = order.indexOf(a.dataset.column);
            const bIndex = order.indexOf(b.dataset.column);
            return aIndex - bIndex;
        });
        
        sortedHeaders.forEach(th => this.headerRow.appendChild(th));
        this.headers = sortedHeaders;
        
        // Reorder each row
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td[data-column]'));
            const sortedCells = [...cells].sort((a, b) => {
                const aIndex = order.indexOf(a.dataset.column);
                const bIndex = order.indexOf(b.dataset.column);
                return aIndex - bIndex;
            });
            sortedCells.forEach(td => row.appendChild(td));
        });
    }
    
    setupDragEvents() {
        this.headers.forEach((header, index) => {
            // Skip non-draggable columns (like S.No and Action)
            if (header.dataset.draggable === 'false') return;
            
            header.setAttribute('draggable', 'true');
            header.classList.add('draggable-header');
            
            // Add drag handle icon
            if (!header.querySelector('.drag-handle')) {
                const handle = document.createElement('span');
                handle.className = 'drag-handle';
                handle.innerHTML = '<i class="bi bi-grip-vertical"></i>';
                header.insertBefore(handle, header.firstChild);
            }
            
            header.addEventListener('dragstart', (e) => this.onDragStart(e, index));
            header.addEventListener('dragend', (e) => this.onDragEnd(e));
            header.addEventListener('dragover', (e) => this.onDragOver(e, index));
            header.addEventListener('dragenter', (e) => this.onDragEnter(e, index));
            header.addEventListener('dragleave', (e) => this.onDragLeave(e));
            header.addEventListener('drop', (e) => this.onDrop(e, index));
        });
    }
    
    onDragStart(e, index) {
        this.draggedColumn = this.headers[index];
        this.draggedIndex = index;
        
        // Set drag image
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', index);
        
        // Add dragging class
        setTimeout(() => {
            this.draggedColumn.classList.add('dragging');
        }, 0);
        
        // Highlight droppable areas
        this.headers.forEach(h => {
            if (h !== this.draggedColumn && h.dataset.draggable !== 'false') {
                h.classList.add('drop-target');
            }
        });
    }
    
    onDragEnd(e) {
        if (this.draggedColumn) {
            this.draggedColumn.classList.remove('dragging');
        }
        
        this.headers.forEach(h => {
            h.classList.remove('drop-target', 'drag-over');
        });
        
        this.draggedColumn = null;
        this.draggedIndex = null;
    }
    
    onDragOver(e, index) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }
    
    onDragEnter(e, index) {
        e.preventDefault();
        const target = this.headers[index];
        
        if (target !== this.draggedColumn && target.dataset.draggable !== 'false') {
            target.classList.add('drag-over');
        }
    }
    
    onDragLeave(e) {
        e.target.classList.remove('drag-over');
    }
    
    onDrop(e, targetIndex) {
        e.preventDefault();
        
        const target = this.headers[targetIndex];
        target.classList.remove('drag-over');
        
        if (this.draggedIndex === targetIndex || target.dataset.draggable === 'false') {
            return;
        }
        
        // Swap columns
        this.swapColumns(this.draggedIndex, targetIndex);
        
        // Save new order
        this.saveColumnOrder();
    }
    
    swapColumns(fromIndex, toIndex) {
        const tbody = this.table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        // Swap headers
        const fromHeader = this.headers[fromIndex];
        const toHeader = this.headers[toIndex];
        
        // Animate swap
        fromHeader.style.transition = 'transform 0.2s ease';
        toHeader.style.transition = 'transform 0.2s ease';
        
        if (fromIndex < toIndex) {
            this.headerRow.insertBefore(fromHeader, toHeader.nextSibling);
        } else {
            this.headerRow.insertBefore(fromHeader, toHeader);
        }
        
        // Update headers array
        this.headers = Array.from(this.headerRow.querySelectorAll('th[data-column]'));
        
        // Swap cells in each row
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td[data-column]'));
            const fromCell = cells[fromIndex];
            const toCell = cells[toIndex];
            
            if (fromCell && toCell) {
                if (fromIndex < toIndex) {
                    row.insertBefore(fromCell, toCell.nextSibling);
                } else {
                    row.insertBefore(fromCell, toCell);
                }
            }
        });
        
        // Remove transition after animation
        setTimeout(() => {
            fromHeader.style.transition = '';
            toHeader.style.transition = '';
        }, 200);
    }
    
    // Reset to default order
    resetOrder() {
        localStorage.removeItem(this.storageKey);
        location.reload();
    }
}

// ============================================
// CSS for Draggable Headers
// ============================================

const draggableStyles = document.createElement('style');
draggableStyles.textContent = `
    .draggable-header {
        cursor: grab;
        user-select: none;
        position: relative;
    }
    
    .draggable-header:active {
        cursor: grabbing;
    }
    
    .draggable-header .drag-handle {
        opacity: 0;
        margin-right: 6px;
        color: var(--zoho-text-muted);
        transition: opacity 0.2s;
    }
    
    .draggable-header:hover .drag-handle {
        opacity: 1;
    }
    
    .draggable-header.dragging {
        opacity: 0.5;
        background: var(--zoho-accent) !important;
    }
    
    .draggable-header.drop-target {
        border-left: 2px dashed var(--zoho-border-light);
        border-right: 2px dashed var(--zoho-border-light);
    }
    
    .draggable-header.drag-over {
        background: rgba(59, 130, 246, 0.2) !important;
        border-left: 3px solid var(--zoho-accent);
    }
    
    /* Column reorder animation */
    .zoho-table th, .zoho-table td {
        transition: transform 0.2s ease;
    }
`;
document.head.appendChild(draggableStyles);

// ============================================
// Initialize Draggable Tables
// ============================================

function initDraggableTable(tableId, tableName) {
    return new DraggableTable(tableId, tableName, '/user/save-column-order/');
}
