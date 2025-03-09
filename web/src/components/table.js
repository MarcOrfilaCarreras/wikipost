import React, { useState } from 'react';

const TableComponent = ({ data = [], columns = [], rowsPerPage = 10, onRowSelect }) => {
    const [currentPage, setCurrentPage] = useState(1);
    const [selectedRows, setSelectedRows] = useState([]);

    const indexOfLastRow = currentPage * rowsPerPage;
    const indexOfFirstRow = indexOfLastRow - rowsPerPage;
    const currentRows = data.slice(indexOfFirstRow, indexOfLastRow);

    const totalPages = Math.ceil(data.length / rowsPerPage);

    const handlePageChange = (page) => {
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
        }
    };

    const handleSelectRow = (row) => {
        const updatedSelectedRows = selectedRows.includes(row)
            ? selectedRows.filter((r) => r !== row)
            : [...selectedRows, row];
        setSelectedRows(updatedSelectedRows);
        if (onRowSelect) {
            onRowSelect(updatedSelectedRows);
        }
    };

    const handleSelectAll = () => {
        let newSelectedRows;
        if (currentRows.every(row => selectedRows.includes(row))) {
            newSelectedRows = selectedRows.filter(row => !currentRows.includes(row));
        } else {
            newSelectedRows = [...selectedRows];
            currentRows.forEach(row => {
                if (!newSelectedRows.includes(row)) {
                    newSelectedRows.push(row);
                }
            });
        }
        setSelectedRows(newSelectedRows);
        if (onRowSelect) {
            onRowSelect(newSelectedRows);
        }
    };

    return (
        <div className="overflow-hidden rounded-lg shadow-lg bg-gray-700">
            <div className="overflow-x-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                <table className="w-full h-full bg-transparent text-sm">
                    <thead className="bg-gray-700">
                        <tr>
                            <th className="px-4 py-3 text-left font-medium text-gray-300 border-b border-gray-700">
                                <input
                                    type="checkbox"
                                    onChange={handleSelectAll}
                                    checked={
                                        currentRows.length > 0 &&
                                        currentRows.every((row) => selectedRows.includes(row))
                                    }
                                    className="cursor-pointer"
                                />
                            </th>
                            {columns.map((column, index) => (
                                <th
                                    key={index}
                                    className="px-6 py-3 text-left font-medium text-gray-300 uppercase tracking-wider border-b border-gray-700"
                                >
                                    {column}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {currentRows.map((row, index) => (
                            <tr
                                key={index}
                                className="hover:bg-gray-600 transition-all duration-300 cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800"
                            >
                                <td className="px-4 py-4 border-b border-gray-700">
                                    <input
                                        type="checkbox"
                                        onChange={() => handleSelectRow(row)}
                                        checked={selectedRows.includes(row)}
                                        className="cursor-pointer"
                                    />
                                </td>
                                {columns.map((column, idx) => (
                                    <td
                                        key={idx}
                                        className="px-6 py-4 text-gray-200 whitespace-nowrap border-b border-gray-700"
                                    >
                                        {row[column]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="flex justify-between items-center m-4">
                <span
                    onClick={() => handlePageChange(currentPage - 1)}
                    className={`cursor-pointer ${currentPage === 1 ? 'opacity-50' : ''}`}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="w-6 h-6 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M15 19l-7-7 7-7"
                        />
                    </svg>
                </span>

                <span className="text-sm text-gray-300">
                    Page {currentPage} of {totalPages}
                </span>

                <span
                    onClick={() => handlePageChange(currentPage + 1)}
                    className={`cursor-pointer ${currentPage === totalPages ? 'opacity-50' : ''}`}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="w-6 h-6 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M9 5l7 7-7 7"
                        />
                    </svg>
                </span>
            </div>
        </div>
    );
};

export default TableComponent;
