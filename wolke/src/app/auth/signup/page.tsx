"use client";

import Link from "next/link";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { object, ref, string } from "yup";
import { usePageTitle } from "@/hooks/usePageTitle";
import { useRouter } from "next/navigation";
import { SignUpFormData } from "@/data/types";
import { useSignUp } from "@/resources/auth";
import { strongPasswordHint, strongPasswordSchema } from "@/data/schema/auth";
import { OAuthButtons } from "@/components/auth/oauth";
import "./academy-auth.css";

const schema = object().shape({
  name: string().required("First name is required"),
  surname: string().required("Last name is required"),
  email: string().email("Enter a valid email").required("Email is required"),
  phone_number: string().matches(
    /^(?:\+?258)?8[2-7]\d{7}$/,
    "Enter a valid Mozambican phone number",
  ),
  password: strongPasswordSchema,
  passwordConfirmation: string()
    .required("Please confirm your password")
    .oneOf([ref("password"), ""], "Passwords must match"),
});

export default function SignUp() {
  usePageTitle("Signup");

  const {
    mutate,
    error,
    reset: resetMutation,
    isPending: loading,
    isError,
  } = useSignUp();

  const {
    register,
    handleSubmit,
    reset: resetForm,
    formState: { errors },
  } = useForm<SignUpFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      name: "",
      surname: "",
      email: "",
      phone_number: "",
      password: "",
      passwordConfirmation: "",
    },
  });
  const router = useRouter();
  const authError = error?.message;

  const signup = async (payload: SignUpFormData) => {
    resetMutation();
    const referralCode = new URLSearchParams(window.location.search).get(
      "referral_code",
    );

    mutate(
      {
        ...payload,
        ...(referralCode ? { referral_code: referralCode } : {}),
      },
      {
        onSuccess: ({ data }) => {
          resetForm();
          router.push(data?.access ? "/auth/verify-email/request" : "/");
        },
      },
    );
  };

  const nameField = register("name");
  const surnameField = register("surname");
  const emailField = register("email");
  const phoneNumberField = register("phone_number");
  const passwordField = register("password");
  const passwordConfirmationField = register("passwordConfirmation");
  const [showPw1, setShowPw1] = useState(false);
  const [showPw2, setShowPw2] = useState(false);

  return (
    <div className="academy-auth">
      <a className="brand" href="/">
        <img src="/wolke-logo-black.svg" alt="Wolke" />
      </a>

      <div className="card signup-card">
        <h1 className="card-title">Criar conta</h1>
        <p className="card-sub">Crie a sua conta para continuar</p>

        <div className="oauth-stack">
          <OAuthButtons />
        </div>

        <div className="divider">
          <span>ou</span>
        </div>

        {isError && authError ? (
          <div className="form-errors">{authError}</div>
        ) : null}

        <form noValidate onSubmit={handleSubmit(signup)}>
          <div className="row">
            <div className="field">
              <label htmlFor="signup-firstname">Nome</label>
              <input
                type="text"
                id="signup-firstname"
                placeholder="João"
                autoComplete="given-name"
                {...nameField}
                onChange={(event) => {
                  if (isError) resetMutation();
                  nameField.onChange(event);
                }}
              />
              {errors.name?.message ? (
                <div className="errors">{errors.name.message}</div>
              ) : null}
            </div>

            <div className="field">
              <label htmlFor="signup-lastname">Apelido</label>
              <input
                type="text"
                id="signup-lastname"
                placeholder="Silva"
                autoComplete="family-name"
                {...surnameField}
                onChange={(event) => {
                  if (isError) resetMutation();
                  surnameField.onChange(event);
                }}
              />
              {errors.surname?.message ? (
                <div className="errors">{errors.surname.message}</div>
              ) : null}
            </div>
          </div>

          <div className="field">
            <label htmlFor="signup-email">
              <span>E-mail</span> <span className="req">*</span>
            </label>
            <input
              type="email"
              id="signup-email"
              placeholder="exemplo@email.com"
              autoComplete="email"
              {...emailField}
              onChange={(event) => {
                if (isError) resetMutation();
                emailField.onChange(event);
              }}
            />
            {errors.email?.message ? (
              <div className="errors">{errors.email.message}</div>
            ) : null}
          </div>

          <div className="field">
            <label htmlFor="signup-phone-number">
              <span>Telefone</span> <span className="req">*</span>
            </label>
            <input
              type="tel"
              id="signup-phone-number"
              placeholder="84 123 4567"
              autoComplete="tel"
              {...phoneNumberField}
              onChange={(event) => {
                if (isError) resetMutation();
                phoneNumberField.onChange(event);
              }}
            />
            {errors.phone_number?.message ? (
              <div className="errors">{errors.phone_number.message}</div>
            ) : null}
          </div>

          <div className="field">
            <label htmlFor="signup-password1">
              <span>Palavra-passe</span> <span className="req">*</span>
            </label>
            <div className="password-wrap">
              <input
                type={showPw1 ? "text" : "password"}
                id="signup-password1"
                placeholder="Crie uma palavra-passe forte"
                autoComplete="new-password"
                {...passwordField}
                onChange={(event) => {
                  if (isError) resetMutation();
                  passwordField.onChange(event);
                }}
              />
              <button
                type="button"
                className="eye-btn"
                aria-label={showPw1 ? "Hide password" : "Show password"}
                onClick={() => setShowPw1((v) => !v)}
              >
                {showPw1 ? (
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
            ) : (
              <p className="hint">{strongPasswordHint}</p>
            )}
          </div>

          <div className="field">
            <label htmlFor="signup-password2">
              <span>Confirmar palavra-passe</span> <span className="req">*</span>
            </label>
            <div className="password-wrap">
              <input
                type={showPw2 ? "text" : "password"}
                id="signup-password2"
                placeholder="Confirme a sua palavra-passe"
                autoComplete="new-password"
                {...passwordConfirmationField}
                onChange={(event) => {
                  if (isError) resetMutation();
                  passwordConfirmationField.onChange(event);
                }}
              />
              <button
                type="button"
                className="eye-btn"
                aria-label={showPw2 ? "Hide password" : "Show password"}
                onClick={() => setShowPw2((v) => !v)}
              >
                {showPw2 ? (
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
            {errors.passwordConfirmation?.message ? (
              <div className="errors">{errors.passwordConfirmation.message}</div>
            ) : null}
          </div>

          <button className="btn" type="submit" disabled={loading}>
            {loading ? "A criar conta..." : "Criar conta"}
          </button>
        </form>

        <div className="card-footer">
          <span>Já tem uma conta?</span> <Link href="/auth/signin">Iniciar sessão</Link>
        </div>
      </div>
    </div>
  );
}
