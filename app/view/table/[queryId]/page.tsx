import { InferGetStaticPropsType, GetStaticProps } from "next";
import { useParams, useSearchParams } from "next/navigation";
import { Table as VizTable, TableProps } from "niagads-viz-js/dist/index"
import * as redis from "redis";

/*import * as Redis from 'ioredis';

const redis = new Redis({
  host: 'localhost', // Replace with your KeyDB host
  port: 6379, // Replace with your KeyDB port
});

async function main() {
  await redis.set('key', 'value');
  const value = await redis.get('key');
  console.log(value); // Output: 'value'
}

main();*/


const cache = redis.createClient({
	url: process.env.API_CACHEDB_URL,
});

/*

// TODO: try - catch around cache query
const getStaticProps = (async (context: any) => {
    //context.params
    const key = "mykey"; // TODO: build key

    await cache.connect();
    const data = await cache.get(key);
    await cache.disconnect()

    if (!data) {
        return { notFound: true}
    }

    return {props: {data}}
}); // satisfies GetStaticProps<{data: TableProps}>
*/
//export default function Table({data,}: InferGetStaticPropsType<typeof getStaticProps>) {
export default function Table() {
	//const params = useParams();
    // const data = params.get("");


	return (
		<main>
            <div>{process.env.API_CACHEDB_URL}</div>
		</main>
	);
}
