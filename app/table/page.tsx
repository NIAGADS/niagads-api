'use client'

import { useSearchParams } from 'next/navigation'
import { Table as VizTable } from 'niagads-viz-js/dist/index'

export default function Table() {
    const params = useSearchParams()
    const data = params.get('data')

    return (
        <main >
         <VizTable id={} columns={} data={}></VizTable>
        </main>
    );
}
