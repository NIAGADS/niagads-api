'use client'

import { useSearchParams } from 'next/navigation'
import { Table as VizTable } from 'niagads-viz-js/dist/index'

export default function Table() {
    const params = useSearchParams()
    const data = params.get('data')

    return (
        <main >
            <div className="pl-8 pt-8">
                <h1 className="text-blue-500">Table!</h1>
            </div>
        </main>
    );
}
