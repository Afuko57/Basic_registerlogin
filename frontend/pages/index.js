import Navbar from "../pages/components/Navbar";
import { useRouter } from 'next/router';

export default function Home() {
  const router = useRouter();
  const { userName } = router.query;

  return (
    <div>
      <Navbar/>
      <title>Homepage</title>
      <div>หน้าแรก</div>
    </div>
  );
}