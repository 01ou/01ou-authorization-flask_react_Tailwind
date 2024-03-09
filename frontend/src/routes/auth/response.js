import { network } from '../../index';
import { redirect } from 'react-router-dom';

export async function authAction(request, url, red) {
  try {
    const formData = Object.fromEntries(await request.formData());
    const response = await fetch(network + url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
      mode: 'cors'
    });

    const result = await response.json();

    if (response.ok) {
      //サインアップ成功

      // ログイン成功時にJWTをローカルストレージに保存する例
      const jwtToken = result.token
      console.log(jwtToken);
      localStorage.setItem('jwtToken', jwtToken);

      return redirect(`${red}`);
    } else {
      console.error('Error:', response.status);
    }

    return result;

  } catch (error) {
    console.error('Error:', error);
    return { error: 'Server not found.' };
  }
}
