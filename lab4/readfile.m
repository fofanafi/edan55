function [ N, p, totalIters, totalMults ] = readfile( filename )

file = fopen(filename);
formatSpec = '%f';
lines_to_read = 1;
Ndata = textscan(file, formatSpec, lines_to_read);
N = Ndata{1};
cdata = textscan(file,'%f %f');
cdata{1} = cdata{1} + 1;
cdata{2} = cdata{2} + 1;
A = sparse(cdata{1}, cdata{2}, 1, N, N);

d = zeros(N,1); % the D matrix, with only one column
deg = zeros(N,1);
for i=1:N
    deg(i) = sum(cdata{1} == i);
    if (deg(i) == 0)
        d(i) = 1/N;
    end
end
[I, J, S] = find(A);
for i=1:length(I)
    S(i) = S(i) / deg(I(i));
end
H = sparse(I, J, S, N, N);

alpha = 0.85;
p = ones(1,N) / N;
plast = ones(1,N) * 100;
totalIters = 0;
totalMults = 0;
while ~withinTolerance(p, plast)
    plast = p;
    p = alpha*p*H + (alpha*p*d + (1-alpha)/N) * ones(1,N);
    totalIters = totalIters + 1;
    totalMults = totalMults + length(I) + N;
end

function [within] = withinTolerance(p, plast)
diff = abs(p - plast) ./ p;

within = all(diff < 0.005);