import { Outlet, redirect } from "react-router-dom";
import { network } from "../..";
import { Header } from '../../components/_index';

export async function loader() {
  const indexEndpoint = '/';
  const jwtToken = localStorage.getItem('jwtToken');
  
  // サーバーにログイン状態を確認
  try {
    const res = await fetch(network + '/check_logging', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${jwtToken}` // AuthorizationヘッダーにBearerスキームでJWTを含める
      }
    });
    if (res.ok) {
      return redirect(indexEndpoint); // 追加: ログイン中は/indexにリダイレクト
    } else {
      throw new Error('Failed to check login status.');
    }
  } catch (error) {
    return null;
  }
}

const RequireNoAuth = () => {
    return (
      <>
        <Header />
        <Outlet />
      </>
    )
}

export default RequireNoAuth;
