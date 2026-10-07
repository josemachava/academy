"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { usePageTitle } from "@/hooks/usePageTitle";
import { boolean, object, string } from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";
import { useSignin } from "@/resources/auth";
import { useRouter, useSearchParams } from "next/navigation";
import { OAuthButtons } from "@/components/auth/oauth";
import "./academy-auth.css";

const schema = object().shape({
  username: string().email("Enter a valid email").required("Email is required"),
  password: string().default(""),
  remember: boolean().default(true),
});

type SigninFormData = {
  username: string;
  password: string;
  remember: boolean;
};

function Signin() {
  const {
    mutate,
    error,
    reset: resetMutation,
    isPending: loading,
    isError,
  } = useSignin();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SigninFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      username: "",
      password: "",
      remember: true,
    },
  });

  const router = useRouter();
  const searchParams = useSearchParams();
  const nextUrl = searchParams.get("next") || "/";

  const signin = async (credentials: SigninFormData) => {
    resetMutation();
    mutate(credentials, {
      onSuccess: () => {
        router.push(nextUrl);
      },
    });
  };

  const authError = error?.message;

  const usernameField = register("username");
  const passwordField = register("password");
  const rememberField = register("remember");
  const [showPassword, setShowPassword] = useState(false);

  usePageTitle("Signin");

  return (
    <div className="academy-auth">
      <a className="brand" href="/">
        <img src="/wolke-logo-black.svg" alt="Wolke" />
      </a>

      <div className="card">
        <h1 className="card-title">Iniciar sessão</h1>
        <p className="card-sub">Bem-vindo de volta. Inicie sessão para continuar</p>

        <div className="oauth-stack">
          <OAuthButtons />
        </div>

        <div className="divider">
          <span>ou</span>
        </div>

        {isError && authError ? (
          <div className="form-errors">{authError}</div>
        ) : null}

        <form method="post" noValidate onSubmit={handleSubmit(signin)}>
          <div className="field">
            <label htmlFor="signin-email">E-mail</label>
            <input
              type="email"
              id="signin-email"
              placeholder="exemplo@email.com"
              autoComplete="email"
              {...usernameField}
              onChange={(event) => {
                if (isError) resetMutation();
                usernameField.onChange(event);
              }}
            />
            {errors.username?.message ? (
              <div className="errors">{errors.username.message}</div>
            ) : null}
          </div>

          <div className="field">
            <div className="label-row">
              <label htmlFor="signin-password">Palavra-passe</label>
              <Link className="forgot-link" href="/auth/password-recovery">
                Esqueceu a palavra-passe?
              </Link>
            </div>
            <div className="password-wrap">
              <input
                type={showPassword ? "text" : "password"}
                id="signin-password"
                placeholder="•••••"
                autoComplete="current-password"
                {...passwordField}
                onChange={(event) => {
                  if (isError) resetMutation();
                  passwordField.onChange(event);
                }}
              />
              <button
                type="button"
                className="eye-btn"
                aria-label={showPassword ? "Hide password" : "Show password"}
                onClick={() => setShowPassword((v) => !v)}
              >
                {showPassword ? (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <path d="M17.94 17.94A10.94 10.94 0 0 1 12 19c-7 0-11-7-11-7a19.86 19.86 0 0 1 5.08-5.9M9.53 9.53A3.2 3.2 0 0 0 12 15.2a3.2 3.2 0 0 0 3.47-3.47" />
                    <path d="M1 1l22 22" />
                  </svg>
                ) : (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z" />
                    <circle cx="12" cy="12" r="3.2" />
                  </svg>
                )}
              </button>
            </div>
            {errors.password?.message ? (
              <div className="errors">{errors.password.message}</div>
            ) : null}
          </div>

          <div className="check-field" style={{ marginBottom: "0.4rem" }}>
            <input
              type="checkbox"
              id="signin-remember"
              {...rememberField}
              onChange={(event) => {
                if (isError) resetMutation();
                rememberField.onChange(event);
              }}
            />
            <label htmlFor="signin-remember">Manter sessão iniciada</label>
          </div>

          <button className="btn" type="submit" disabled={loading}>
            {loading ? "A entrar..." : "Entrar"}
          </button>
        </form>

        <div className="card-footer">
          <span>Não tem uma conta?</span> <Link href="/auth/signup">Criar conta agora</Link>
        </div>
      </div>
    </div>
  );
}

export default function SignInPage() {
  return (
    <Suspense>
      <Signin />
    </Suspense>
  );
}
