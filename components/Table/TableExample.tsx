import React from 'react';
import Table from './Table';
import './Table.css';

/**
 * 表格组件使用示例
 * 
 * 功能说明：
 * 1. 支持多选（复选框）
 * 2. 支持开关切换
 * 3. 包含四个状态列，每个状态列支持四种状态类型：
 *    - success（成功）- 绿色
 *    - warning（警告）- 橙色
 *    - error（错误）- 红色
 *    - info（信息）- 蓝色
 * 4. 支持分页功能
 * 5. 响应式设计
 */
const TableExample: React.FC = () => {
  return (
    <div style={{ padding: '20px', width: '100%', height: '100vh' }}>
      <h1 style={{ marginBottom: '20px', fontFamily: 'Microsoft YaHei', fontSize: '18px' }}>
        数据表格示例
      </h1>
      <Table />
    </div>
  );
};

export default TableExample;

