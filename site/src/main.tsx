import React from 'react';
import { createRoot } from 'react-dom/client';
import '../app/globals.css';
import './fonts.css';
import Home from '../app/page';

function Disclaimer() {
  return (
    <footer
      style={{
        maxWidth: 1180,
        margin: '32px auto 40px',
        padding: '16px 20px',
        fontSize: 12.5,
        lineHeight: 1.6,
        color: '#666',
        borderTop: '1px solid #e5e5e5',
      }}
    >
      <p style={{ margin: 0 }}>
        이 사이트는 배예림(Yerim Bae)의 개인 리서치 프로젝트입니다. 자료는 금융정보분석원(FIU) 신고 명단(2026-08-31 기준)과
        DART 공시(감사보고서·사업보고서)에서 확인한 사실, 그 요약, 그리고 분석적 추론을 구분해 표시합니다.
        &ldquo;분석&rdquo;으로 표시된 내용은 감사보고서에 직접 기재된 사실이 아니라 공개 자료를 바탕으로 한 개인 의견이며,
        특정 회사에 대한 평가나 투자 판단의 근거로 쓰일 수 없습니다. 오류를 발견하시면{' '}
        <a href="https://github.com/yerim-Bae/vasp-audit-map" target="_blank" rel="noreferrer" style={{ color: '#9F3F2F' }}>GitHub 저장소</a>로 알려주세요.
      </p>
      <p style={{ margin: '8px 0 0' }}>
        만든 과정(출처 우선순위, 법인 매칭, 사실·추론 구분, 품질검사)과 데이터·소스 코드는{' '}
        <a href="https://github.com/yerim-Bae/vasp-audit-map" target="_blank" rel="noreferrer" style={{ color: '#9F3F2F' }}>github.com/yerim-Bae/vasp-audit-map</a>에
        있습니다. © 2026 Yerim Bae
      </p>
    </footer>
  );
}

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Home />
    <Disclaimer />
  </React.StrictMode>,
);
