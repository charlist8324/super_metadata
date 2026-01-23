let currentTableData = null;
let currentUser = null;
let editMode = false;
let editedComments = {};

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function parseDataType(dataType) {
    if (!dataType) {
        return { type: '-', length: '-' };
    }
    
    const match = dataType.match(/^(\w+)(?:\(([^)]+)\))?$/);
    if (match) {
        return {
            type: match[1],
            length: match[2] || '-'
        };
    }
    
    return { type: dataType, length: '-' };
}

async function loadTableDetails(tableId) {
    try {
        const response = await fetch(`/api/tables/${tableId}`);
        if (!response.ok) {
            if (response.status === 401) {
                alert('请先登录');
                window.location.href = '/login';
                return;
            }
            const errorData = await response.json().catch(() => ({ error: '未知错误' }));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const table = await response.json();
        currentTableData = table;
        
        // 更新页面标题
        document.getElementById('tableTitle').textContent = `表: ${table.table_name}`;
        document.title = `${table.table_name} - 表详情 - Super MetaData 元数据管理系统`;
        
        // 更新基本信息
        document.getElementById('detailTableName').textContent = table.table_name;
        document.getElementById('detailSchemaName').textContent = table.schema_name || '-';
        document.getElementById('detailRowCount').textContent = table.row_count?.toLocaleString() || '未知';
        document.getElementById('detailSizeBytes').textContent = formatBytes(table.size_bytes || 0);
        document.getElementById('detailComment').textContent = table.comment || '无';
        document.getElementById('detailCreatedAt').textContent = table.created_at ? new Date(table.created_at).toLocaleString() : '未知';
        document.getElementById('detailUpdatedAt').textContent = table.updated_at ? new Date(table.updated_at).toLocaleString() : '未知';
        
        // 加载字段信息
        loadColumns(table.columns);
        
    } catch (error) {
        console.error('加载表详情失败:', error);
        alert('加载表详情失败: ' + error.message);
    }
}

function loadColumns(columns) {
    const tbody = document.getElementById('columnsList');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (!columns || columns.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-3 text-muted">暂无字段信息</td></tr>';
        return;
    }
    
    columns.forEach(column => {
        const parsedType = parseDataType(column.data_type);
        const row = document.createElement('tr');
        row.dataset.columnId = column.id;
        
        // 注释列根据编辑模式显示不同内容
        const commentCell = editMode 
            ? `<input type="text" class="form-control form-control-sm" 
                       data-column-id="${column.id}" 
                       value="${column.column_comment || ''}" 
                       placeholder="输入注释（留空表示删除注释）" 
                       onchange="updateEditedComment(${column.id}, this.value)">`
            : `<span class="comment-display">${column.column_comment || '-'}</span>`;
        
        row.innerHTML = `
            <td>${column.column_name}</td>
            <td>${parsedType.type}</td>
            <td>${parsedType.length}</td>
            <td>${column.is_nullable === 'YES' ? '是' : '否'}</td>
            <td>${column.default_value || '-'}</td>
            <td>${column.ordinal_position || '-'}</td>
            <td>${commentCell}</td>
        `;
        tbody.appendChild(row);
    });
    
    // 根据用户权限显示编辑按钮
    const editBtn = document.getElementById('editColumnsBtn');
    const saveBtn = document.getElementById('saveColumnsBtn');
    const cancelBtn = document.getElementById('cancelEditBtn');
    
    if (editBtn && saveBtn && cancelBtn) {
        if (currentUser && (currentUser.role === 'admin' || currentUser.role === 'user')) {
            editBtn.style.display = 'block';
        } else {
            editBtn.style.display = 'none';
            saveBtn.style.display = 'none';
            cancelBtn.style.display = 'none';
        }
    }
    
    // 更新表格的编辑模式样式
    const table = document.getElementById('columnsTable');
    if (table) {
        if (editMode) {
            table.classList.add('edit-mode');
        } else {
            table.classList.remove('edit-mode');
        }
    }
}

// 更新编辑的注释
function updateEditedComment(columnId, value) {
    editedComments[columnId] = value;
}

// 切换编辑模式
function toggleEditMode() {
    editMode = !editMode;
    editedComments = {};
    
    if (editMode) {
        document.getElementById('editColumnsBtn').style.display = 'none';
        document.getElementById('saveColumnsBtn').style.display = 'block';
        document.getElementById('cancelEditBtn').style.display = 'block';
    } else {
        document.getElementById('editColumnsBtn').style.display = 'block';
        document.getElementById('saveColumnsBtn').style.display = 'none';
        document.getElementById('cancelEditBtn').style.display = 'none';
        editedComments = {};
    }
    
    // 重新加载字段列表
    if (currentTableData) {
        loadColumns(currentTableData.columns);
    }
}

// 保存字段注释
async function saveColumnComments() {
    if (Object.keys(editedComments).length === 0) {
        alert('没有需要保存的注释');
        return;
    }
    
    try {
        const response = await fetch('/api/columns/comments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                comments: editedComments
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert(result.message || '注释保存成功！');
            editMode = false;
            editedComments = {};
            document.getElementById('editColumnsBtn').style.display = 'block';
            document.getElementById('saveColumnsBtn').style.display = 'none';
            document.getElementById('cancelEditBtn').style.display = 'none';
            
            // 重新加载表详情
            if (currentTableData) {
                await loadTableDetails(currentTableData.id);
            }
        } else {
            alert('保存失败: ' + (result.error || '未知错误'));
        }
    } catch (error) {
        console.error('保存注释失败:', error);
        alert('保存注释失败: ' + error.message);
    }
}

function checkAuthStatus() {
    fetch('/api/current-user')
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('未登录');
        })
        .then(userData => {
            currentUser = userData;
            showUserMenu(userData);
        })
        .catch(error => {
            console.error('检查登录状态失败:', error);
            showLoginMenu();
        });
}

function showUserMenu(userData) {
    document.getElementById('usernameDisplay').textContent = userData.full_name || userData.username;
    document.getElementById('mainNavMenu').classList.remove('d-none');
    document.getElementById('userMenu').classList.remove('d-none');
    document.getElementById('loginMenu').classList.add('d-none');
}

function showLoginMenu() {
    document.getElementById('mainNavMenu').classList.remove('d-none');
    document.getElementById('userMenu').classList.add('d-none');
    document.getElementById('loginMenu').classList.remove('d-none');
}

async function logout() {
    if (!confirm('确定要退出登录吗？')) {
        return;
    }
    
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            window.location.href = '/';
        } else {
            alert('退出登录失败');
        }
    } catch (error) {
        console.error('退出登录失败:', error);
        alert('退出登录失败');
    }
}

function showUserInfo() {
    alert('功能开发中：显示用户详细信息');
}