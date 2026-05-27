import dynamic from "next/dynamic";
import styles from "./page.module.css";

export default function Home() {
	const API = dynamic(() => import("../components/StoplightDocs"), {
		ssr: false,
	});
	return;

	<API />;
}
