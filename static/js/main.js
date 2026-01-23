// 全局变量
let currentTableId = null;

// 格式化数据大小
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// 显示加载状态
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">加载中...</span></div></div>';
    }
}

// 显示错误消息
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="alert alert-danger" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>${message}</div>`;
    }
}

// 显示成功消息
function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="alert alert-success" role="alert"><i class="fas fa-check-circle me-2"></i>${message}</div>`;
    }
}

// 加载数据源列表
async function loadDataSources() {
    try {
        const tbody = document.querySelector('#dataSourcesTable tbody');
        if (!tbody) return;
        
        // 显示加载状态到tbody中
        tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">加载中...</span></div></td></tr>';
        
        const response = await fetch('/api/data-sources');
        const dataSources = await response.json();
        
        tbody.innerHTML = '';
        
        dataSources.forEach(source => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${source.id}</td>
                <td>${source.name}</td>
                <td><span class="badge bg-secondary">${source.type.toUpperCase()}</span></td>
                <td>${source.host}</td>
                <td>${source.port}</td>
                <td>${source.database}</td>
                <td>${new Date(source.created_at).toLocaleString()}</td>
                <td class="operations">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editDataSource(${source.id})">
                        <i class="fas fa-edit"></i> 编辑
                    </button>
                    <button class="btn btn-sm btn-outline-danger me-1" onclick="deleteDataSource(${source.id})">
                        <i class="fas fa-trash"></i> 删除
                    </button>
                    <button class="btn btn-sm btn-outline-success me-1" onclick="testConnection(${source.id})">
                        <i class="fas fa-plug"></i> 测试
                    </button>
                    <button class="btn btn-sm btn-outline-info" onclick="extractMetadata(${source.id})">
                        <i class="fas fa-download"></i> 抽数
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('加载数据源失败:', error);
        const tbody = document.querySelector('#dataSourcesTable tbody');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4">${error.message}</td></tr>`;
        }
    }
}

// 编辑数据源
async function editDataSource(id) {
    try {
        const response = await fetch(`/api/data-sources/${id}`);
        const dataSource = await response.json();
        
        document.getElementById('dataSourceId').value = dataSource.id;
        document.getElementById('name').value = dataSource.name;
        document.getElementById('type').value = dataSource.type;
        document.getElementById('host').value = dataSource.host;
        document.getElementById('port').value = dataSource.port;
        document.getElementById('username').value = dataSource.username;
        document.getElementById('password').value = dataSource.password;
        document.getElementById('database').value = dataSource.database;
        
        document.getElementById('modalTitle').textContent = '编辑数据源';
        document.getElementById('password').removeAttribute('required'); // 编辑时密码不是必填
        
        const modal = new bootstrap.Modal(document.getElementById('addDataSourceModal'));
        modal.show();
    } catch (error) {
        console.error('获取数据源信息失败:', error);
        alert('获取数据源信息失败: ' + error.message);
    }
}

// 删除数据源
async function deleteDataSource(id) {
    if (!confirm('确定要删除这个数据源吗？此操作不可恢复！')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/data-sources/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(result.message || '数据源删除成功！');
            loadDataSources(); // 刷新列表
        } else {
            const error = await response.json();
            alert('删除失败: ' + error.error);
        }
    } catch (error) {
        console.error('删除数据源失败:', error);
        alert('删除数据源失败: ' + error.message);
    }
}

// 测试连接
async function testConnection(id) {
    try {
        const response = await fetch(`/api/data-sources/${id}/test`);
        const result = await response.json();
        
        if (result.success) {
            alert('连接测试成功！');
        } else {
            alert('连接测试失败: ' + result.error);
        }
    } catch (error) {
        console.error('连接测试失败:', error);
        alert('连接测试失败: ' + error.message);
    }
}

// 抽取元数据
async function extractMetadata(id) {
    if (!confirm('确定要抽取此数据源的元数据吗？此操作可能需要一些时间。')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/data-sources/${id}/extract`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // 检查响应是否为JSON格式
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const result = await response.json();
            
            if (response.ok) {
                alert('元数据抽取成功！');
            } else {
                alert('元数据抽取失败: ' + (result.error || '未知错误'));
            }
        } else {
            // 如果不是JSON格式，说明返回了HTML错误页面
            const text = await response.text();
            console.error('服务器返回非JSON格式响应:', text);
            alert('元数据抽取失败: 服务器返回错误响应');
        }
    } catch (error) {
        console.error('元数据抽取失败:', error);
        alert('元数据抽取失败: ' + error.message);
    }
}

// 保存数据源
async function saveDataSource() {
    const id = document.getElementById('dataSourceId').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/data-sources/${id}` : '/api/data-sources';
    
    const dataSourceData = {
        name: document.getElementById('name').value,
        type: document.getElementById('type').value,
        host: document.getElementById('host').value,
        port: parseInt(document.getElementById('port').value),
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        database: document.getElementById('database').value
    };
    
    // 如果是编辑且密码为空，则不发送密码字段
    if (id && !dataSourceData.password) {
        delete dataSourceData.password;
    }
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataSourceData)
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(result.message || (id ? '数据源更新成功！' : '数据源添加成功！'));
            
            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('addDataSourceModal'));
            modal.hide();
            
            // 清空表单
            document.getElementById('dataSourceForm').reset();
            document.getElementById('dataSourceId').value = '';
            document.getElementById('modalTitle').textContent = '添加数据源';
            document.getElementById('password').setAttribute('required', '');
            
            // 刷新列表
            loadDataSources();
        } else {
            const error = await response.json();
            alert('保存失败: ' + error.error);
        }
    } catch (error) {
        console.error('保存数据源失败:', error);
        alert('保存数据源失败: ' + error.message);
    }
}

// 加载数据源列表用于元数据页面
async function loadDataSourcesForMetadata() {
    try {
        const response = await fetch('/api/data-sources');
        const dataSources = await response.json();
        
        const select = document.getElementById('dataSourceSelect');
        if (!select) return;
        
        select.innerHTML = '<option value="">请选择数据源</option>';
        
        dataSources.forEach(source => {
            const option = document.createElement('option');
            option.value = source.id;
            option.textContent = `${source.name} (${source.type.toUpperCase()} - ${source.host}:${source.port}/${source.database})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('加载数据源失败:', error);
    }
}

// 加载表列表
async function loadTables() {
    const dataSourceId = document.getElementById('dataSourceSelect').value;
    
    if (!dataSourceId) {
        document.getElementById('tablesList').innerHTML = '';
        document.getElementById('tableDetailsSection').style.display = 'none';
        return;
    }
    
    try {
        // 显示加载状态到tbody中
        const tbody = document.getElementById('tablesList');
        if (!tbody) return;
        
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">加载中...</span></div></td></tr>';
        
        const response = await fetch(`/api/data-sources/${dataSourceId}/tables`);
        const result = await response.json();
        const tables = result.tables;
        
        tbody.innerHTML = '';
        
        if (!tables || tables.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-muted">暂无表数据，请执行ETL任务抽取元数据</td></tr>';
            return;
        }
        
        tables.forEach(table => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${table.table_name}</td>
                <td>${table.schema_name || '-'}</td>
                <td>${table.row_count?.toLocaleString() || '0'}</td>
                <td>${(table.size_bytes || 0) === 0 ? '-' : formatBytes(table.size_bytes)}</td>
                <td>${table.comment || '-'}</td>
                <td>${table.created_at ? new Date(table.created_at).toLocaleString() : '-'}</td>
                <td class="operations">
                    <div class="d-flex justify-content-center">
                        <a href="/table/${table.id}" class="btn btn-sm btn-outline-primary" title="查看详情">
                            <i class="fas fa-eye"></i>
                        </a>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('加载表列表失败:', error);
        const tbody = document.getElementById('tablesList');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger py-4">加载表列表失败: ${error.message}</td></tr>`;
        }
    }
}

// 查看表详细信息
async function viewTableDetails(tableId, tableName) {
    console.log('查看表详情:', tableId, tableName);
    currentTableId = tableId;
    
    try {
        // 显示表详细信息部分
        const detailsSection = document.getElementById('tableDetailsSection');
        if (detailsSection) {
            detailsSection.style.display = 'block';
            
            // 滚动到详情区域
            detailsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        // 更新基本表信息
        const selectedTableTitle = document.getElementById('selectedTableTitle');
        if (selectedTableTitle) {
            selectedTableTitle.textContent = `表: ${tableName}`;
        }
        const detailTableName = document.getElementById('detailTableName');
        if (detailTableName) {
            detailTableName.textContent = tableName;
        }
        
        // 获取完整的表信息
        const response = await fetch(`/api/tables/${tableId}`);
        if (!response.ok) {
            if (response.status === 401) {
                alert('请先登录后再查看表详情');
                window.location.href = '/login';
                return;
            }
            const errorData = await response.json().catch(() => ({ error: '未知错误' }));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        const table = await response.json();
        
        if (detailTableName) {
            detailTableName.textContent = table.table_name;
        }
        document.getElementById('detailSchemaName').textContent = table.schema_name || '-';
        document.getElementById('detailRowCount').textContent = table.row_count?.toLocaleString() || '未知';
        document.getElementById('detailSizeBytes').textContent = formatBytes(table.size_bytes || 0);
        document.getElementById('detailComment').textContent = table.comment || '无';
        document.getElementById('detailCreatedAt').textContent = table.created_at ? new Date(table.created_at).toLocaleString() : '未知';
        document.getElementById('detailUpdatedAt').textContent = table.updated_at ? new Date(table.updated_at).toLocaleString() : '未知';
        
        // 加载字段信息
        await loadColumns(tableId);
        
        // 计算字段统计信息
        if (table.columns) {
            calculateColumnStatistics(table.columns);
        }
        
    } catch (error) {
        console.error('加载表详细信息失败:', error);
        alert('加载表详细信息失败: ' + error.message);
    }
}

// 解析数据类型，返回类型和长度
function parseDataType(dataType) {
    if (!dataType) {
        return { type: '-', length: '-' };
    }
    
    // 匹配类似 VARCHAR(255)、INT(11)、DECIMAL(10,2) 的格式
    const match = dataType.match(/^(\w+)(?:\(([^)]+)\))?$/);
    if (match) {
        return {
            type: match[1],
            length: match[2] || '-'
        };
    }
    
    return { type: dataType, length: '-' };
}

// 加载字段列表
async function loadColumns(tableId) {
    try {
        const response = await fetch(`/api/tables/${tableId}`);
        const table = await response.json();
        
        const columns = table.columns || [];
        const relationships = table.relationships || [];
        
        const tbody = document.getElementById('columnsList');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (columns.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-3 text-muted">暂无字段信息</td></tr>';
            return;
        }
        
        columns.forEach(column => {
            const parsedType = parseDataType(column.data_type);
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${column.column_name}</td>
                <td>${parsedType.type}</td>
                <td>${parsedType.length}</td>
                <td>${column.is_nullable === 'YES' ? '是' : '否'}</td>
                <td>${column.default_value || '-'}</td>
                <td>${column.ordinal_position || '-'}</td>
                <td>${column.column_comment || '-'}</td>
            `;
            tbody.appendChild(row);
        });
        
        // 加载关联关系信息
        loadRelationships(relationships);
    } catch (error) {
        console.error('加载字段列表失败:', error);
        const tbody = document.getElementById('columnsList');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center py-3 text-danger">加载字段列表失败</td></tr>';
        }
    }
}

// 加载关联关系信息
function loadRelationships(relationships) {
    const tbody = document.getElementById('relationshipsList');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (relationships.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-3 text-muted">暂无关联关系</td></tr>';
        return;
    }
    
    relationships.forEach(rel => {
        const row = document.createElement('tr');
        
        let direction, fromInfo, toInfo;
        
        if (rel.type === 'outgoing') {
            direction = '→';
            fromInfo = `${rel.column_name}`;
            toInfo = `${rel.referenced_table_name}.${rel.referenced_column_name}`;
        } else {
            direction = '←';
            fromInfo = `${rel.referencing_table_name}.${rel.referencing_column_name}`;
            toInfo = `${rel.column_name}`;
        }
        
        row.innerHTML = `
            <td>${rel.constraint_name || '-'}</td>
            <td>${fromInfo}</td>
            <td>${direction}</td>
            <td>${toInfo}</td>
            <td>${rel.constraint_type || 'FOREIGN KEY'}</td>
        `;
        tbody.appendChild(row);
    });
}

// 计算字段统计信息
function calculateColumnStatistics(columns) {
    const stats = {};
    
    columns.forEach(column => {
        if (stats[column.data_type]) {
            stats[column.data_type]++;
        } else {
            stats[column.data_type] = 1;
        }
    });
    
    const tbody = document.getElementById('columnsSummaryBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    for (const [dataType, count] of Object.entries(stats)) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${dataType}</td>
            <td>${count}</td>
        `;
        tbody.appendChild(row);
    }
}

// 隐藏表详细信息
function hideTableDetails() {
    document.getElementById('tableDetailsSection').style.display = 'none';
}



// 加载抽取历史
async function loadHistory(page = 1) {
    const dataSourceFilter = document.getElementById('historyDataSourceFilter').value;
    const statusFilter = document.getElementById('historyStatusFilter').value;
    const pageSize = document.getElementById('pageSize').value || 20;
    
    try {
        showLoading('historyTable');
        
        let url = `/api/extraction-history?page=${page}&per_page=${pageSize}`;
        if (dataSourceFilter) {
            url += `&datasource_id=${dataSourceFilter}`;
        }
        if (statusFilter) {
            url += `&status=${statusFilter}`;
        }
        
        const response = await fetch(url);
        const result = await response.json();
        
        const history = result.history;
        const totalPages = result.pagination.pages;
        
        const tbody = document.querySelector('#historyTable tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        history.forEach(record => {
            const row = document.createElement('tr');
            
            // 根据状态设置不同样式
            let statusHtml = '';
            if (record.status === 'success') {
                statusHtml = `<span class="badge bg-success">成功</span>`;
            } else if (record.status === 'failed') {
                statusHtml = `<span class="badge bg-danger">失败</span>`;
            } else {
                statusHtml = `<span class="badge bg-secondary">${record.status}</span>`;
            }
            
            row.innerHTML = `
                <td>${record.id}</td>
                <td>${record.datasource_name}</td>
                <td>${new Date(record.extraction_time).toLocaleString()}</td>
                <td>${statusHtml}</td>
                <td>${record.extracted_tables}</td>
                <td>${record.total_tables || '-'}</td>
                <td>${record.duration || '-'}</td>
                <td>${record.message || '-'}</td>
            `;
            tbody.appendChild(row);
        });
        
        // 更新分页控件
        updatePagination(page, totalPages);
    } catch (error) {
        console.error('加载抽取历史失败:', error);
        showError('historyTable', '加载抽取历史失败: ' + error.message);
    }
}

// 更新分页控件
function updatePagination(currentPage, totalPages) {
    const paginationNav = document.getElementById('paginationNav');
    const paginationList = document.getElementById('paginationList');
    
    if (!paginationList) return;
    
    paginationList.innerHTML = '';
    
    if (totalPages <= 1) {
        paginationNav.style.display = 'none';
        return;
    }
    
    paginationNav.style.display = 'block';
    
    // 上一页按钮
    if (currentPage > 1) {
        const prevLi = document.createElement('li');
        prevLi.className = 'page-item';
        prevLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${currentPage - 1})">上一页</a>`;
        paginationList.appendChild(prevLi);
    } else {
        const prevLi = document.createElement('li');
        prevLi.className = 'page-item disabled';
        prevLi.innerHTML = `<span class="page-link">上一页</span>`;
        paginationList.appendChild(prevLi);
    }
    
    // 页码按钮
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        const pageLi = document.createElement('li');
        pageLi.className = i === currentPage ? 'page-item active' : 'page-item';
        pageLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${i})">${i}</a>`;
        paginationList.appendChild(pageLi);
    }
    
    // 下一页按钮
    if (currentPage < totalPages) {
        const nextLi = document.createElement('li');
        nextLi.className = 'page-item';
        nextLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${currentPage + 1})">下一页</a>`;
        paginationList.appendChild(nextLi);
    } else {
        const nextLi = document.createElement('li');
        nextLi.className = 'page-item disabled';
        nextLi.innerHTML = `<span class="page-link">下一页</span>`;
        paginationList.appendChild(nextLi);
    }
}

// 跳转到指定页面
function goToPage(page) {
    loadHistory(page);
    
    // 滚动到表格顶部
    document.querySelector('#historyTable').scrollIntoView({ behavior: 'smooth' });
}

// 过滤历史记录
function filterHistory() {
    const searchInput = document.getElementById("historySearch");
    const dataSourceFilter = document.getElementById("historyDataSourceFilter");
    const statusFilter = document.getElementById("historyStatusFilter");
    const searchFilter = searchInput.value.toLowerCase();
    const dataSourceFilterValue = dataSourceFilter.value;
    const statusFilterValue = statusFilter.value;
    const table = document.getElementById("historyTable");
    const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        const datasourceCell = cells[1]; // 数据源列
        const statusCell = cells[3]; // 状态列
        
        let showRow = true;
        
        // 检查搜索关键词
        if (searchFilter && datasourceCell.textContent.toLowerCase().indexOf(searchFilter) === -1) {
            showRow = false;
        }
        
        // 检查数据源筛选
        if (dataSourceFilterValue && datasourceCell.textContent.toLowerCase().indexOf(dataSourceFilterValue) === -1) {
            showRow = false;
        }
        
        // 检查状态筛选
        if (statusFilterValue && !statusCell.textContent.includes(statusFilterValue)) {
            showRow = false;
        }
        
        rows[i].style.display = showRow ? "" : "none";
    }
}

// 加载ETL任务列表
async function loadETLTasks() {
    try {
        const tbody = document.getElementById('tasksList');
        if (!tbody) return;
        
        tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">加载中...</span></div></td></tr>';
        
        const response = await fetch('/api/etl-tasks');
        const tasks = await response.json();
        
        tbody.innerHTML = '';
        
        tasks.forEach(task => {
            const row = document.createElement('tr');
            
            // 根据状态设置不同样式
            let statusHtml = '';
            if (task.status === 'active') {
                statusHtml = `<span class="badge bg-success">启用</span>`;
            } else {
                statusHtml = `<span class="badge bg-secondary">禁用</span>`;
            }
            
            row.innerHTML = `
                <td>${task.id}</td>
                <td>${task.name}</td>
                <td>${task.dataSource}</td>
                <td>${task.schedule}</td>
                <td>${statusHtml}</td>
                <td>${task.lastRun || '-'}</td>
                <td>${task.nextRun || '-'}</td>
                <td class="operations">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editETLTask(${task.id})">
                        <i class="fas fa-edit"></i> 编辑
                    </button>
                    <button class="btn btn-sm btn-outline-danger me-1" onclick="deleteETLTask(${task.id})">
                        <i class="fas fa-trash"></i> 删除
                    </button>
                    <button class="btn btn-sm btn-outline-success" onclick="executeETLTask(${task.id})">
                        <i class="fas fa-play"></i> 执行
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('加载ETL任务失败:', error);
        const tbody = document.getElementById('tasksList');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4">加载ETL任务失败: ${error.message}</td></tr>`;
        }
    }
}

// 编辑ETL任务
async function editETLTask(id) {
    try {
        const response = await fetch(`/api/etl-tasks/${id}`);
        const task = await response.json();
        
        document.getElementById('taskId').value = task.id;
        document.getElementById('taskName').value = task.name;
        document.getElementById('taskType').value = task.type;
        document.getElementById('dataSource').value = task.dataSourceId;
        document.getElementById('scheduleType').value = task.scheduleType;
        document.getElementById('taskStatus').value = task.status;
        document.getElementById('description').value = task.description;
        
        document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit me-2"></i><span>编辑ETL任务</span>';
        
        // 显示相应的调度字段
        toggleScheduleFields();
        
        const modal = new bootstrap.Modal(document.getElementById('addETLTaskModal'));
        modal.show();
    } catch (error) {
        console.error('获取ETL任务信息失败:', error);
        alert('获取ETL任务信息失败: ' + error.message);
    }
}

// 删除ETL任务
async function deleteETLTask(id) {
    if (!confirm('确定要删除这个ETL任务吗？此操作不可恢复！')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/etl-tasks/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(result.message);
            loadETLTasks(); // 刷新列表
        } else {
            const error = await response.json();
            alert('删除失败: ' + error.error);
        }
    } catch (error) {
        console.error('删除ETL任务失败:', error);
        alert('删除ETL任务失败: ' + error.message);
    }
}

// 保存ETL任务
async function saveETLTask() {
    const id = document.getElementById('taskId').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/etl-tasks/${id}` : '/api/etl-tasks';
    
    const taskData = {
        name: document.getElementById('taskName').value,
        type: document.getElementById('taskType').value,
        dataSourceId: document.getElementById('dataSource').value,
        scheduleType: document.getElementById('scheduleType').value,
        status: document.getElementById('taskStatus').value,
        description: document.getElementById('description').value
    };
    
    // 根据调度类型添加相应字段
    const scheduleType = document.getElementById('scheduleType').value;
    if (scheduleType === 'interval') {
        taskData.intervalValue = document.getElementById('intervalValue').value;
        taskData.intervalUnit = document.getElementById('intervalUnit').value;
    } else if (scheduleType === 'cron') {
        taskData.cronExpression = document.getElementById('cronExpression').value;
    }
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(result.message);
            
            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('addETLTaskModal'));
            modal.hide();
            
            // 清空表单
            document.getElementById('etlTaskForm').reset();
            document.getElementById('taskId').value = '';
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle me-2"></i><span>添加ETL任务</span>';
            
            // 刷新列表
            loadETLTasks();
        } else {
            const error = await response.json();
            alert('保存失败: ' + error.error);
        }
    } catch (error) {
        console.error('保存ETL任务失败:', error);
        alert('保存ETL任务失败: ' + error.message);
    }
}

// 执行ETL任务
async function executeETLTask(id) {
    if (!confirm('确定要立即执行这个ETL任务吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/etl-tasks/${id}/execute`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(result.message);
        } else {
            const error = await response.json();
            alert('执行失败: ' + error.error);
        }
    } catch (error) {
        console.error('执行ETL任务失败:', error);
        alert('执行ETL任务失败: ' + error.message);
    }
}

// 任务搜索过滤功能
function filterTasks() {
    const input = document.getElementById("taskSearch");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("etlTasksTable");
    const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        let found = false;
        
        for (let j = 0; j < cells.length - 1; j++) { // 不搜索操作列
            if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }
        
        if (found) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
}

// 切换调度字段显示
function toggleScheduleFields() {
    const scheduleType = document.getElementById('scheduleType').value;
    document.getElementById('intervalFields').style.display = 'none';
    document.getElementById('cronFields').style.display = 'none';
    
    if (scheduleType === 'interval') {
        document.getElementById('intervalFields').style.display = 'block';
    } else if (scheduleType === 'cron') {
        document.getElementById('cronFields').style.display = 'block';
    }
}

// 加载概览数据
async function loadOverviewData() {
    try {
        const response = await fetch('/api/overview');
        const data = await response.json();

        // 更新统计数字
        document.getElementById('dataSourcesCount').textContent = data.data_sources_count;
        document.getElementById('tablesCount').textContent = data.tables_count;
        document.getElementById('columnsCount').textContent = data.columns_count;
        document.getElementById('extractedTablesCount').textContent = data.total_extracted_tables;

        // 更新最近活动表格
        const activityBody = document.getElementById('recentActivityBody');
        if (activityBody && data.recent_extraction) {
            activityBody.innerHTML = `
                <tr>
                    <td class="fw-medium">${data.recent_extraction.datasource_name}</td>
                    <td>${new Date(data.recent_extraction.extraction_time).toLocaleTimeString()}</td>
                    <td>
                        <span class="badge ${
                            data.recent_extraction.status === 'success' ? 'bg-success' : 
                            data.recent_extraction.status === 'failed' ? 'bg-danger' : 'bg-secondary'
                        }">${data.recent_extraction.status}</span>
                    </td>
                </tr>
            `;
        } else if (activityBody) {
            activityBody.innerHTML = '<tr><td colspan="3" class="text-center py-4 text-muted">暂无抽取记录</td></tr>';
        }
    } catch (error) {
        console.error('加载概览数据失败:', error);
        // 显示错误信息
        document.querySelectorAll('[id$="Count"]').forEach(el => el.textContent = '错误');
        const activityBody = document.getElementById('recentActivityBody');
        if (activityBody) {
            activityBody.innerHTML = '<tr><td colspan="3" class="text-center py-4 text-danger">加载数据失败</td></tr>';
        }
    }
}

// 表格搜索过滤功能
function filterTables() {
    const input = document.getElementById("tableSearch");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("tablesList");
    const rows = table.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        let found = false;
        
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }
        
        if (found) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
}

// 检查用户登录状态
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/current-user');
        if (response.ok) {
            const userData = await response.json();
            showUserMenu(userData);
            return true;
        } else {
            showLoginMenu();
            return false;
        }
    } catch (error) {
        console.error('检查登录状态失败:', error);
        showLoginMenu();
        return false;
    }
}

// 显示用户菜单
function showUserMenu(userData) {
    document.getElementById('usernameDisplay').textContent = userData.full_name || userData.username;
    document.getElementById('mainNavMenu').classList.remove('d-none');
    document.getElementById('userMenu').classList.remove('d-none');
    document.getElementById('loginMenu').classList.add('d-none');
}

// 显示登录菜单
function showLoginMenu() {
    document.getElementById('mainNavMenu').classList.remove('d-none');
    document.getElementById('userMenu').classList.add('d-none');
    document.getElementById('loginMenu').classList.remove('d-none');
}

// 登出功能
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

// 显示用户信息
function showUserInfo() {
    alert('功能开发中：显示用户详细信息');
}