import { useEffect, useState } from 'react';
import './notice.css';

/*
  첫 방문 안내 창 (A안).
  닫기 — 이번 방문에만 닫습니다. 새로 들어오면 다시 보입니다.
  오늘 하루 보지 않기 — 그날 자정까지 localStorage 에 저장해 두고 띄우지 않습니다.
  하단 "안내 다시 보기" 링크가 window 이벤트 'vasp-notice:open' 을 보내면 다시 엽니다.
*/
const KEY = 'vaspmap-notice-until';

function suppressedNow(): boolean {
  try {
    return Date.now() < Number(localStorage.getItem(KEY) || 0);
  } catch {
    return false;
  }
}

export default function Notice() {
  const [mounted, setMounted] = useState(false);
  const [on, setOn] = useState(false);

  const open = () => {
    setMounted(true);
    setTimeout(() => setOn(true), 20);
  };
  const shut = () => {
    setOn(false);
    setTimeout(() => setMounted(false), 260);
  };
  const later = () => {
    const d = new Date();
    d.setHours(24, 0, 0, 0);
    try {
      localStorage.setItem(KEY, String(d.getTime()));
    } catch {
      /* 저장 못 해도 닫기는 동작 */
    }
    shut();
  };

  useEffect(() => {
    if (!suppressedNow()) open();
    const onOpen = () => open();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') shut();
    };
    window.addEventListener('vasp-notice:open', onOpen);
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('vasp-notice:open', onOpen);
      window.removeEventListener('keydown', onKey);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!mounted) return null;
  return (
    <>
      <div className={`nt-veil${on ? ' on' : ''}`} onClick={shut} />
      <aside className={`nt${on ? ' on' : ''}`} role="dialog" aria-modal="false" aria-labelledby="ntTitle">
        <p className="nt-kicker">안내</p>
        <p className="nt-lead" id="ntTitle">
          국내 VASP 사업·회계 지도는
          <br />
          가상자산사업자 45곳의 신고 현황·감사보고서·
          <br />
          회계정책·감사위험을 한 화면에 모은
          <br />
          개인 리서치 프로젝트입니다.
        </p>
        <p>
          모든 내용은 감사보고서 원문에서 확인한 <b>사실</b>,
          <br />
          그 <b>요약</b>, 그리고 제 <b>분석</b>을 구분해 표시합니다.
          <br />
          &ldquo;분석&rdquo;은 감사보고서에 적힌 사실이 아닌 개인 의견입니다.
        </p>
        <p>
          <b>이런 분께 유용합니다.</b> 가상자산 회사 감사를 처음 맡은 회계사,
          <br />
          회사마다 다른 가상자산 회계처리를 비교하고 싶은 분,
          <br />
          거래소의 사업구조를 공시로 확인하고 싶은 분.
        </p>
        <p>
          <b>이렇게 쓰시면 됩니다.</b> 왼쪽 목록에서 회사를 고르면
          <br />
          &ldquo;어떻게 돈을 버나&rdquo;부터 순서대로 읽힙니다.
          <br />
          상단 <b>거래소 5개사 비교</b>에서 회계처리 차이를 한눈에 보고,
          <br />
          원문 인용의 접수번호를 누르면 DART 원문으로 이동합니다.
        </p>
        <div className="nt-acts">
          <button type="button" className="nt-later" onClick={later}>
            오늘 하루 보지 않기
          </button>
          <button type="button" className="nt-close" onClick={shut} autoFocus>
            닫고 둘러보기
          </button>
        </div>
      </aside>
    </>
  );
}
