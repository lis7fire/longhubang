public class baidu {
	private static String getbaidu(String j, String r) {
		Integer[] a = new Integer[256];
		Integer[] p = new Integer[256];
		String o = "";
		int v = j.length();
		for (int q = 0; q < 256; q++) {
			int z = q % v;
			String js = j.substring(z, z + 1);
			int jc = (int) js.charAt(0);
			a[q] = jc;
			p[q] = q;
		}
		for (int u = 0, q = 0; q < 256; q++) {
			u = (u + p[q] + a[q]) % 256;
			int t = p[q];
			p[q] = p[u];
			p[u] = t;
		}
		for (int i = 0, u = 0, q = 0; i < r.length(); q++) {
			i = (i + 1) % 256;
			u = (u + p[i]) % 256;
			int t = p[i];
			p[i] = p[u];
			p[u] = t;
			int k = p[(p[i] + p[u]) % 256];
			int kr = r.charAt(q) ^ k;
			o += (char) kr + "";
		}
		return o;
	}

	private static String base64(String G) {
		String C = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
		int _ = G.length();
		System.out.println(_);
		int A = 0;
		String B = "";
		while (A < _) {
			int F = G.charAt(A++) & 255;
			if (A == _) {
				B += C.charAt(F >> 2);
				B += C.charAt((F & 3) << 4);
				B += "==";
				break;
			}
			int D = G.charAt(A++);
			if (A == _) {
				B += C.charAt(F >> 2);
				B += C.charAt(((F & 3) << 4) | ((D & 240) >> 4));
				B += C.charAt((D & 15) << 2);
				B += "=";
				break;
			}
			int E = G.charAt(A++);
			B += C.charAt(F >> 2);
			B += C.charAt(((F & 3) << 4) | ((D & 240) >> 4));
			B += C.charAt(((D & 15) << 2) | ((E & 192) >> 6));
			B += C.charAt(E & 63);
		}
		return B;
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String sign1 = "cc942f3a1311109b3e40e2ff5a1a3ba75f135b5e";
		String sign3 = "d76a889b6aafd3o87ac3bd56f4d4053a";
		String sign4 = "d76a889b6aafd3o87ac3bd56f4d4053a";
		String sign5 = "d76e889b6aafd3087ac3bd56f4d4053a";
		String sign = "IQN3FHjbuvdW6cM52575rHCNuTitLJXZbgYpbMhj5hBNVnZerV21Nw==";
		// sign =
		// getbaidu("e8c7d729eea7b54551aa594f942decbe","e788ed448ae1fa5cfe980b77ac2ea9afd8a9148a");
		sign = getbaidu("d76e889b6aafd3087ac3bd56f4d4053a",
				"2adfe3f9fbafb38fa08582de625346015ca13ce9");
		System.out.println(sign);
		System.out.println(base64(sign));
	}
}
