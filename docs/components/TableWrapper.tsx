"use client";

import Table, { TableProps, TableConfig } from "@niagads/table";

export default function TableWrapper({ id, data, columns }: TableProps) {
	const defaultColumns = columns.map((c: any, index) => {
		if (index < 8 || c["id"].startsWith("num_") || c["id"] === "url")
			return c["id"];
	});
	const options: TableConfig = {
		disableColumnFilters: true,
		defaultColumns: defaultColumns,
	};
	return <Table id={id} data={data} columns={columns} options={options} />;
}
