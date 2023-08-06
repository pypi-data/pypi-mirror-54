% Data from
%  https://medium.com/@nykolas.z/dns-resolvers-performance-compared-cloudflare-x-google-x-quad9-x-opendns-149e803734e5

% Features:           privacy     DNSCrypt    DNSoverHTTPS    DNSoverTLS
% Google                  X           -               X           X
% CloudFlare              X           -               X           X
% Quad9                   X           -               -           X
% OpenDNS                 -           X               -           X
% Norton                  -           -               -           -
% CleanBrowsing           X           X               X           -
% Yandex                  -           -               -           -
% Comodo                  -           X               -           X

% Latency Average (ms):      Global    North America    Europe
% Google                      16.44           8.53       7.17
% CloudFlare                   4.98           3.93       2.96
% Quad9                       18.25           7.21       4.35
% OpenDNS                     46.51          14.66       8.99
% Norton                      34.75           8.32      10.35
% CleanBrowsing               19.14          11.83       5.74
% Yandex                     169.91         119.09      35.74
% Comodo                      71.90          25.91      13.06
%                   Mean:     47.735         24.935     11.045


rel("Google",("privacy";"DNSoverHTTPS";"DNSoverTLS")).
rel("Cloudflare",("privacy";"DNSoverHTTPS";"DNSoverTLS")).
rel("Quad9",("privacy";"DNSoverTLS")).
rel("OpenDNS",("DNSCrypt";"DNSoverTLS")).
obj("Norton").
rel("CleanBrowsing",("privacy";"DNSCrypt";"DNSoverHTTPS")).
obj("Yandex").
rel("Comodo",("DNSCrypt";"DNSoverTLS")).
