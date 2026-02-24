import React, { useState } from 'react';
import './Table.css';

// 状态类型定义
type StatusType = 'success' | 'warning' | 'error' | 'info';

interface TableRow {
  id: string;
  title: string;
  enabled: boolean;
  description: string;
  status1: StatusType;
  status2: StatusType;
  status3: StatusType;
  status4: StatusType;
}

// 状态徽标组件
interface StatusBadgeProps {
  status: StatusType;
  label: string;
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label }) => {
  const getStatusColor = (status: StatusType) => {
    switch (status) {
      case 'success':
        return '#2CAF5E'; // 绿色
      case 'warning':
        return '#FF9C01'; // 橙色
      case 'error':
        return '#EA3636'; // 红色
      case 'info':
        return '#3A84FF'; // 蓝色
      default:
        return '#979BA5'; // 灰色
    }
  };

  return (
    <div className="status-badge">
      <div className="status-badge-content">
        <div className="status-icon-wrapper">
          <div 
            className="status-dot" 
            style={{ backgroundColor: getStatusColor(status) }}
          />
        </div>
        <span className="status-label">{label}</span>
      </div>
    </div>
  );
};

// 开关组件
interface SwitchProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
}

const Switch: React.FC<SwitchProps> = ({ checked, onChange }) => {
  return (
    <div 
      className={`switch ${checked ? 'switch-on' : 'switch-off'}`}
      onClick={() => onChange(!checked)}
    >
      <div className="switch-dot" />
    </div>
  );
};

// 复选框组件
interface CheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
}

const Checkbox: React.FC<CheckboxProps> = ({ checked, onChange }) => {
  return (
    <div 
      className={`checkbox ${checked ? 'checkbox-checked' : ''}`}
      onClick={() => onChange(!checked)}
    >
      {checked && <span className="checkbox-checkmark">✓</span>}
    </div>
  );
};

// 表格组件
const Table: React.FC = () => {
  const [rows, setRows] = useState<TableRow[]>([
    { id: '1', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'success', status2: 'warning', status3: 'error', status4: 'info' },
    { id: '2', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'success', status2: 'info', status3: 'warning', status4: 'success' },
    { id: '3', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'warning', status2: 'error', status3: 'info', status4: 'warning' },
    { id: '4', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'error', status2: 'success', status3: 'success', status4: 'error' },
    { id: '5', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'info', status2: 'warning', status3: 'error', status4: 'info' },
    { id: '6', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'success', status2: 'success', status3: 'info', status4: 'warning' },
    { id: '7', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'warning', status2: 'info', status3: 'success', status4: 'error' },
    { id: '8', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'error', status2: 'error', status3: 'warning', status4: 'success' },
    { id: '9', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'info', status2: 'success', status3: 'error', status4: 'info' },
    { id: '10', title: 'Blue King', enabled: true, description: 'Blue King', status1: 'success', status2: 'warning', status3: 'info', status4: 'warning' },
  ]);

  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;
  const totalItems = 198;

  const handleRowSelect = (id: string) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedRows(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedRows.size === rows.length) {
      setSelectedRows(new Set());
    } else {
      setSelectedRows(new Set(rows.map(row => row.id)));
    }
  };

  const handleToggleSwitch = (id: string) => {
    setRows(rows.map(row => 
      row.id === id ? { ...row, enabled: !row.enabled } : row
    ));
  };

  const getStatusLabel = (status: StatusType) => {
    switch (status) {
      case 'success':
        return '成功';
      case 'warning':
        return '警告';
      case 'error':
        return '错误';
      case 'info':
        return '信息';
      default:
        return '未知';
    }
  };

  return (
    <div className="table-container">
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th className="table-header checkbox-header">
                <Checkbox 
                  checked={selectedRows.size === rows.length && rows.length > 0}
                  onChange={handleSelectAll}
                />
              </th>
              <th className="table-header">Title</th>
              <th className="table-header">开关</th>
              <th className="table-header">描述</th>
              <th className="table-header">状态1</th>
              <th className="table-header">状态2</th>
              <th className="table-header">状态3</th>
              <th className="table-header">状态4</th>
              <th className="table-header">操作</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="table-row">
                <td className="table-cell checkbox-cell">
                  <Checkbox 
                    checked={selectedRows.has(row.id)}
                    onChange={() => handleRowSelect(row.id)}
                  />
                </td>
                <td className="table-cell">{row.title}</td>
                <td className="table-cell switch-cell">
                  <Switch 
                    checked={row.enabled}
                    onChange={(checked) => handleToggleSwitch(row.id)}
                  />
                </td>
                <td className="table-cell">{row.description}</td>
                <td className="table-cell status-cell">
                  <StatusBadge status={row.status1} label={getStatusLabel(row.status1)} />
                </td>
                <td className="table-cell status-cell">
                  <StatusBadge status={row.status2} label={getStatusLabel(row.status2)} />
                </td>
                <td className="table-cell status-cell">
                  <StatusBadge status={row.status3} label={getStatusLabel(row.status3)} />
                </td>
                <td className="table-cell status-cell">
                  <StatusBadge status={row.status4} label={getStatusLabel(row.status4)} />
                </td>
                <td className="table-cell action-cell">
                  <a href="#" className="action-link">操作</a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 设置按钮 */}
      <div className="table-setting">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M7 8.75C7.9665 8.75 8.75 7.9665 8.75 7C8.75 6.0335 7.9665 5.25 7 5.25C6.0335 5.25 5.25 6.0335 5.25 7C5.25 7.9665 6.0335 8.75 7 8.75Z" fill="#C4C6CC"/>
          <path d="M7 1.75C7.41421 1.75 7.75 1.41421 7.75 1C7.75 0.585786 7.41421 0.25 7 0.25C6.58579 0.25 6.25 0.585786 6.25 1C6.25 1.41421 6.58579 1.75 7 1.75Z" fill="#C4C6CC"/>
          <path d="M7 13.75C7.41421 13.75 7.75 13.4142 7.75 13C7.75 12.5858 7.41421 12.25 7 12.25C6.58579 12.25 6.25 12.5858 6.25 13C6.25 13.4142 6.58579 13.75 7 13.75Z" fill="#C4C6CC"/>
          <path d="M1 7C1 7.41421 1.33579 7.75 1.75 7.75C2.16421 7.75 2.5 7.41421 2.5 7C2.5 6.58579 2.16421 6.25 1.75 6.25C1.33579 6.25 1 6.58579 1 7Z" fill="#C4C6CC"/>
          <path d="M11.5 7C11.5 7.41421 11.8358 7.75 12.25 7.75C12.6642 7.75 13 7.41421 13 7C13 6.58579 12.6642 6.25 12.25 6.25C11.8358 6.25 11.5 6.58579 11.5 7Z" fill="#C4C6CC"/>
          <path d="M2.5 2.5C2.5 2.91421 2.83579 3.25 3.25 3.25C3.66421 3.25 4 2.91421 4 2.5C4 2.08579 3.66421 1.75 3.25 1.75C2.83579 1.75 2.5 2.08579 2.5 2.5Z" fill="#C4C6CC"/>
          <path d="M10 2.5C10 2.91421 10.3358 3.25 10.75 3.25C11.1642 3.25 11.5 2.91421 11.5 2.5C11.5 2.08579 11.1642 1.75 10.75 1.75C10.3358 1.75 10 2.08579 10 2.5Z" fill="#C4C6CC"/>
          <path d="M10 11.5C10 11.9142 10.3358 12.25 10.75 12.25C11.1642 12.25 11.5 11.9142 11.5 11.5C11.5 11.0858 11.1642 10.75 10.75 10.75C10.3358 10.75 10 11.0858 10 11.5Z" fill="#C4C6CC"/>
          <path d="M2.5 11.5C2.5 11.9142 2.83579 12.25 3.25 12.25C3.66421 12.25 4 11.9142 4 11.5C4 11.0858 3.66421 10.75 3.25 10.75C2.83579 10.75 2.5 11.0858 2.5 11.5Z" fill="#C4C6CC"/>
        </svg>
      </div>

      {/* 分页 */}
      <div className="table-pagination">
        <div className="pagination-info">
          <span>共计 {totalItems} 条</span>
          <span>每页</span>
          <select className="page-size-select">
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
          <span>条</span>
        </div>
        <div className="pagination-controls">
          <button className="pagination-btn" disabled={currentPage === 1}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M10 12L6 8L10 4" stroke="#979BA5" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          <button className={`pagination-btn ${currentPage === 1 ? 'active' : ''}`}>1</button>
          <button className={`pagination-btn ${currentPage === 2 ? 'active' : ''}`}>2</button>
          <button className={`pagination-btn ${currentPage === 3 ? 'active' : ''}`}>3</button>
          <button className={`pagination-btn ${currentPage === 4 ? 'active' : ''}`}>4</button>
          <button className={`pagination-btn ${currentPage === 5 ? 'active' : ''}`}>5</button>
          <button className="pagination-btn">...</button>
          <button className="pagination-btn">20</button>
          <button className="pagination-btn" disabled={currentPage === 20}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M6 4L10 8L6 12" stroke="#979BA5" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Table;

